import inspect
import sqlite3
from sqlite3 import Row
from typing import Optional
from src.mixins.query_builder_mixin import QueryBuilderMixin
from src.libraries.table import TableBase
from src.utils.helpers import regexp
from src.models import tables


class Database(QueryBuilderMixin):
    conn: Optional[sqlite3.Connection] = None

    @classmethod
    def create_connection(cls, db_host: str):
        try:
            cls.conn = sqlite3.connect(db_host)
            cls.conn.create_function("REGEXP", 2, regexp)
            cls.create_tables()
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def close_connection(cls):
        if cls.conn:
            cls.conn.close()
        else:
            print("There is no open connection")

    @classmethod
    def create_tables(cls):
        classes_info = cls.__get_tables_info()

        for subject in classes_info:
            if subject["base_classes"][0] is TableBase:
                cls.create_table(subject["class"]).run()

    @classmethod
    def run(cls) -> int:
        """Executes query and returns number of affected rows"""
        cursor = cls.conn.cursor()
        query = cls.build()

        if query.parameters:
            if isinstance(query.parameters, list):
                cursor.executemany(query.statement, query.parameters)
            else:
                cursor.execute(query.statement, query.parameters)
        else:
            cursor.execute(query.statement)

        cls.conn.commit()
        results = cursor.rowcount
        cursor.close()
        return results

    @classmethod
    def get(cls) -> list[Row]:
        cursor = cls.conn.cursor()
        query = cls.build()

        if query.parameters:
            cursor.execute(query.statement, query.parameters)
        else:
            cursor.execute(query.statement)

        cursor.row_factory = sqlite3.Row
        result = cursor.fetchall()
        cursor.close()
        return result

    @classmethod
    def get_one(cls) -> Row:
        cursor = cls.conn.cursor()
        query = cls.build()

        if query.parameters:
            cursor.execute(query.statement, query.parameters)
        else:
            cursor.execute(query.statement)

        cursor.row_factory = sqlite3.Row
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def __get_tables_info() -> list:
        classes_info = []

        for name, obj in inspect.getmembers(tables, inspect.isclass):
            # Gather information about the class
            class_info = {
                "name": name,
                "class": obj,
                "base_classes": obj.__bases__,
                "attributes": [attr for attr in dir(obj) if not attr.startswith("__")],
            }
            classes_info.append(class_info)
            classes_info.reverse()

        return classes_info
