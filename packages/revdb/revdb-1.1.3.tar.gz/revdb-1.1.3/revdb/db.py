import copy
import datetime
import uuid
from functools import partial
from typing import Any, Dict, Type, TypeVar

import requests
from bson.objectid import ObjectId
from mongoengine import Document, DynamicDocument, IntField, ObjectIdField, StringField
from mongoengine import connect as mongo_connect  # ignore: type
from mongoengine.base import BaseDocument
from pymongo import IndexModel, MongoClient
from typing_extensions import Protocol

URLS_V1 = {
    "stg": "https://jstorage-stg.revtel-api.com/v1",
    "prod": "https://jstorage.revtel-api.com/v1",
}

_db_hosts: Dict[str, Any] = {}


def default_timestamp() -> int:
    now = datetime.datetime.utcnow()
    return int(round(now.timestamp() * 1000))


def _get_v1_host(stage: str) -> str:
    try:
        return URLS_V1[stage]
    except KeyError as exc:
        raise ValueError("stage should be in [stg, prod]") from exc


def connect(
    client_id: str, client_secret: str, stage: str = "stg", alias: str = "default"
) -> MongoClient:
    host = _get_v1_host(stage)
    key = f"{client_id}__{alias}"

    try:
        db = _db_hosts[key]
    except KeyError:
        full_url = (
            f"{host}/settings?client_secret={client_secret}&client_id={client_id}"
        )
        resp = requests.get(full_url)
        resp.raise_for_status()

        resp_json = resp.json()
        db = mongo_connect(
            resp_json["client_id"], host=resp_json["db_host"], alias=alias
        )
        _db_hosts[key] = db

    return db


DOC = TypeVar("DOC", bound=BaseDocument)


def from_collection(
    collection: str,
    stage: str = "stg",
    alias: str = "default",
    offline: bool = False,
    offline_host: bool = False,
    client_id: str = "",
    client_secret: str = "",
    db_host: str = "",
    **meta: Any,
) -> Type[BaseDocument]:
    def save_with_updated(self: BaseDocument, *args: Any, **kwargs: Any) -> Any:
        setattr(self, "updated", default_timestamp())
        return DynamicDocument.save(self, *args, **kwargs)

    def unique_key() -> str:
        return uuid.uuid4().__str__()  # pragma: nocover

    alias = f"{client_id}__{alias}"

    if not offline:
        host = _get_v1_host(stage)
        url = f"{host}/collection/{collection}?client_id={client_id}&client_secret={client_secret}"

        resp = requests.get(url)
        resp.raise_for_status()
        resp_json = resp.json()

        pk_name = resp_json["primary_key"]
    else:
        pk_name = meta.pop("default_pk", None)

    if offline_host:
        mongo_connect(client_id, host=db_host, alias=alias)
    else:
        connect(client_id, client_secret, stage=stage, alias=alias)

    namespace = {
        "meta": {
            **meta,
            "collection": collection,
            "db_alias": alias,
            "id_field": "_obj_id",
        },
        pk_name: StringField(unique=True, default=unique_key),
        "_obj_id": ObjectIdField(default=ObjectId, primary_key=True),
        "created": IntField(default=default_timestamp),
        "updated": IntField(default=default_timestamp),
        "save": save_with_updated,
    }

    doc_cls = type(f"{client_id}__{collection}", (DynamicDocument,), namespace)

    if doc_cls._meta.get("abstract"):
        return doc_cls

    _collection = doc_cls._get_collection()  # type: ignore
    indexes = dict(_collection.index_information())
    index = IndexModel(
        [(pk_name, 1)],
        unique=True,
        partialFilterExpression={pk_name: {"$type": "string"}},
    )

    if (
        f"{pk_name}_1" in indexes
        and "partialFilterExpression" not in indexes[f"{pk_name}_1"]
    ):
        _collection.drop_index(f"{pk_name}_1")
        _collection.create_indexes([index])
    elif f"{pk_name}_1" not in indexes:
        _collection.create_indexes([index])

    return doc_cls


class FactoryProtocol(Protocol):
    def __call__(
        self, collection: str, alias: str = "default", **kwargs: Any
    ) -> Type[DynamicDocument]:
        pass  # pragma: no cover


def collection_factory(
    client_secret: str, client_id: str, stage: str = "stg"
) -> FactoryProtocol:
    return partial(
        from_collection, client_id=client_id, client_secret=client_secret, stage=stage
    )


def offline_database(
    client_id: str, db_host: str, default_pk: str = "id"
) -> FactoryProtocol:
    return partial(
        from_collection,
        client_id=client_id,
        offline=True,
        db_host=db_host,
        offline_host=True,
        default_pk=default_pk,
    )


def make_model_class(base: Type[DOC], **meta: Any) -> Type[DOC]:
    return type(base.__name__, (base,), {"meta": meta})


def create_connected_model(
    doc_class: BaseDocument, client_id: str, host: str, **kwargs: Any
) -> BaseDocument:
    db = client_id
    alias = f"{db}_alias"

    copy_class = copy.deepcopy(doc_class)
    copy_class.__name__ = f"{db}__{doc_class.__name__}"

    mongo_connect(db, host=host, alias=alias)
    return make_model_class(copy_class, db_alias=alias, **kwargs)


class ModelMixin:
    _meta: Dict[str, Any]

    @classmethod
    def from_client(cls, client_id: str) -> BaseDocument:
        db_host = cls._meta.get("db_host")
        if not db_host:
            raise ValueError("should define db_host in meta")

        return create_connected_model(
            cls,
            host=db_host,
            client_id=client_id,
        )


class Model(ModelMixin, DynamicDocument):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}


class StrictModel(ModelMixin, Document):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}
