from dataclasses import dataclass
from typing import Optional
from src.libraries.table import TableBase


@dataclass
class Query:
    statement: str
    parameters: Optional[list | tuple | dict]


class DataType:
    @staticmethod
    def integer(null: bool = True, default: Optional[str | int] = None,
                primary_key: bool = False, autoincrement: bool = False):
        return (
            f"INTEGER{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
            f"{" PRIMARY KEY" if primary_key else ""}"
            f"{" AUTOINCREMENT" if autoincrement else ""}"
        )

    @staticmethod
    def text(null: bool = True, default: Optional[str | int] = None):
        return (
            f"TEXT{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )

    @staticmethod
    def datetime(null: bool = True, default: Optional[str | int] = "CURRENT_TIMESTAMP"):
        return (
            f"DATETIME{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )

    @staticmethod
    def blob(null: bool = True, default=None):
        return (
            f"BLOB{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )


class QueryBuilderMixin:
    __statement: Optional[str] = None
    __table: Optional[str] = None
    __parameters: list | dict = []

    @classmethod
    def create_table(cls, table: type[TableBase]):
        create_table = f"CREATE TABLE IF NOT EXISTS {table.name} ("

        for field, parameters in table.fields.items():
            create_table += f"{field} {parameters}, "

        if table.references:
            for reference in table.references:
                create_table += f"FOREIGN KEY ({reference[0]}) REFERENCES {reference[1]}({reference[2]}), "
        cls.__statement = create_table.rstrip(", ") + ")"
        return cls()

    @classmethod
    def select(cls, __from: type[TableBase] | str, fields: dict | tuple):
        select = "SELECT "
        cls.__table = __from if isinstance(__from, str) else __from.name

        if isinstance(fields, dict):
            for table in fields.keys():
                for column in fields[table]:
                    select += f"{table}.{column}, "
        else:
            for column in fields:
                select += f"{cls.__table}.{column}, "

        cls.__statement = f"{select.rstrip(", ")} FROM {cls.__table}"
        return cls()

    @classmethod
    def insert(cls, table: type[TableBase] | str, fields: tuple,  values: list | tuple, ignore: bool = False):
        vals = f"{tuple(['?' for _ in fields])}".replace("'", "")
        cols = str(fields).replace("'", "")
        cls.__statement = (
            f"INSERT {"OR IGNORE " if ignore else ""}"
            f"INTO {table if isinstance(table, str) else table.name} {cols}"
            f" VALUES {vals}"
        )
        cls.__parameters = values
        return cls()

    @classmethod
    def update(cls, table: type[TableBase] | str, fields: dict):
        update = f"UPDATE {table if isinstance(table, str) else table.name} SET "

        for column in fields.keys():
            update += f"{column} = ?, "

        cls.__statement = f"{update.rstrip(", ")}"
        cls.__parameters = list(fields.values())
        return cls()

    @classmethod
    def delete(cls, __from: type[TableBase] | str):
        cls.__statement = f"DELETE FROM {__from if isinstance(__from, str) else __from.name}"
        return cls()

    @classmethod
    def inner_join(cls, references: tuple[tuple]):
        for reference in references:
            cls.__statement += (
                f" INNER JOIN {reference[1]} "
                f"ON {cls.__table}.{reference[2]} = {reference[1]}.{reference[0]}"
            )
        return cls()

    @classmethod
    def left_join(cls, references: tuple[tuple]):
        for reference in references:
            cls.__statement += (
                f" LEFT JOIN {reference[1]} "
                f"ON {cls.__table}.{reference[2]} = {reference[1]}.{reference[0]}"
            )
        return cls()

    @classmethod
    def where(cls, condition: str, parameters: list | dict):
        cls.__statement += f" WHERE {condition}"

        if isinstance(parameters, list):
            cls.__parameters += parameters
        else:
            cls.__parameters = parameters
        return cls()

    @classmethod
    def order_by(cls, column: str):
        cls.__statement += f" ORDER BY {column}"
        return cls()

    @classmethod
    def asc(cls):
        cls.__statement += " ASC"
        return cls()

    @classmethod
    def desc(cls):
        cls.__statement += " DESC"
        return cls()

    @classmethod
    def limit(cls, __to: int, __from: int = 0):
        cls.__statement += f" LIMIT {__to if not __from else f"{__from}, {__to}"}"
        return cls()

    @classmethod
    def build(cls):
        list_of_tuples = any(isinstance(item, tuple) for item in cls.__parameters)
        statement = cls.__statement.strip()
        parameters = cls.__parameters if list_of_tuples or isinstance(cls.__parameters, dict) \
            else tuple(cls.__parameters)
        cls.reset_query()
        return Query(statement=statement, parameters=parameters)

    @classmethod
    def reset_query(cls):
        cls.__statement = cls.__table = None
        cls.__parameters = []
