from typing import TypeVar, List, Dict

from peewee import ModelSelect
from database.common.models import BaseModel

from ..common.models import db

T = TypeVar("T")


def store_data(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()


def retrieve_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)
    return response


class CRUDInteface:
    @staticmethod
    def create():
        return store_data

    @staticmethod
    def retrieve():
        return retrieve_data


if __name__ == "__main__":
    store_data()
    retrieve_data()
    CRUDInteface()
