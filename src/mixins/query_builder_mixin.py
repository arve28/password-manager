from dataclasses import dataclass
from typing import Optional
from src.libraries.table import TableBase


@dataclass
class Query:
    """
    Return object for QueryBuilderMixin.build().
    :var statement: Sqlite query.
    :var parameters: Values for query parameters.
    """
    statement: str
    parameters: Optional[list | tuple | dict]


class DataType:
    """Data types for table's columns."""
    @staticmethod
    def integer(null: bool = True, default: Optional[str | int] = None,
                primary_key: bool = False, autoincrement: bool = False) -> str:
        """
        Generates CREATE TABLE sqlite query part that describes INTEGER type column.
        :param null: Null value column.
        :param default: DEFAULT value for column.
        :param primary_key: Set column as PRIMARY KEY.
        :param autoincrement: Set column to be automatically incremented.
        """
        return (
            f"INTEGER{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
            f"{" PRIMARY KEY" if primary_key else ""}"
            f"{" AUTOINCREMENT" if autoincrement else ""}"
        )

    @staticmethod
    def text(null: bool = True, default: Optional[str | int] = None) -> str:
        """
        Generates CREATE TABLE sqlite query part that describes TEXT type column.
        :param null: Null value column.
        :param default: DEFAULT value for column.
        """
        return (
            f"TEXT{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )

    @staticmethod
    def datetime(null: bool = True, default: Optional[str | int] = "CURRENT_TIMESTAMP") -> str:
        """
        Generates CREATE TABLE sqlite query part that describes DATETIME type column.
        :param null: Null value column.
        :param default: DEFAULT value for column.
        """
        return (
            f"DATETIME{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )

    @staticmethod
    def blob(null: bool = True, default=None) -> str:
        """
        Generates CREATE TABLE sqlite query part that describes BLOB type column.
        :param null: Null value column.
        :param default: DEFAULT value for column.
        """
        return (
            f"BLOB{f" DEFAULT {default}" if default is not None else ""}"
            f"{" NOT NULL" if not null else ""}"
        )


class QueryBuilderMixin:
    """
    Class for generating sqlite queries.
    :var __statement: Query statement.
    :var __table: Name of a table.
    :var __parameters: Values for query parameters.
    """
    __statement: Optional[str] = None
    __table: Optional[str] = None
    __parameters: list | dict = []

    @classmethod
    def create_table(cls, table: type[TableBase]):
        """
        Generates CREATE TABLE query.
        :param table: Table model(:class:`TableBase`) object.
        """
        create_table = f"CREATE TABLE IF NOT EXISTS {table.name} ("

        for field, parameters in table.columns.items():
            create_table += f"{field} {parameters}, "

        if table.references:
            for reference in table.references:
                create_table += f"FOREIGN KEY ({reference[0]}) REFERENCES {reference[1]}({reference[2]}), "
        cls.__statement = create_table.rstrip(", ") + ")"
        return cls()

    @classmethod
    def select(cls, __from: type[TableBase] | str, fields: dict | tuple):
        """
        Generates SELECT query.
        :param __from: Table model(:class:`TableBase`) object or table name.
        :param fields: The fields(:class:`TableBase`.selectable) to include in the SELECT query.
        """
        select = "SELECT "
        cls.__table = __from if isinstance(__from, str) else __from.name

        if isinstance(fields, dict):
            for table, columns in fields.items():
                for column in columns:
                    select += f"{table}.{column}, "
        else:
            for column in fields:
                select += f"{cls.__table}.{column}, "

        cls.__statement = f"{select.rstrip(", ")} FROM {cls.__table}"
        return cls()

    @classmethod
    def insert(cls, table: type[TableBase] | str, fields: tuple,  values: list | tuple, ignore: bool = False):
        """
        Generates INSERT query.
        :param table: Table model(:class:`TableBase`) object or table name.
        :param fields: Columns to insert into ("col", ...).
        :param values: Values to insert [(value, ...), ...] or (value, ...).
        :param ignore: Ignore if any constraint is violated.
        """
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
        """
        Generates UPDATE query.
        :param table: Table model(:class:`TableBase`) object or table name.
        :param fields: Columns and values to update - {"col": value, ...}.
        """
        update = f"UPDATE {table if isinstance(table, str) else table.name} SET "

        for column in fields.keys():
            update += f"{column} = ?, "

        cls.__statement = f"{update.rstrip(", ")}"
        cls.__parameters = list(fields.values())
        return cls()

    @classmethod
    def delete(cls, __from: type[TableBase] | str):
        """
        Generates DELETE query.
        :param __from: Table model(:class:`TableBase`) object or table name.
        """
        cls.__statement = f"DELETE FROM {__from if isinstance(__from, str) else __from.name}"
        return cls()

    @classmethod
    def inner_join(cls, references: tuple[tuple]):
        """
        Generates INNER_JOIN statement.
        :param references: Foreign keys - :class:`TableBase`.references.
        """
        for reference in references:
            cls.__statement += (
                f" INNER JOIN {reference[1]} "
                f"ON {cls.__table}.{reference[2]} = {reference[1]}.{reference[0]}"
            )
        return cls()

    @classmethod
    def left_join(cls, references: tuple[tuple]):
        """
        Generates LEF_JOIN statement.
        :param references: Foreign keys - :class:`TableBase`.references.
        """
        for reference in references:
            cls.__statement += (
                f" LEFT JOIN {reference[1]} "
                f"ON {cls.__table}.{reference[2]} = {reference[1]}.{reference[0]}"
            )
        return cls()

    @classmethod
    def where(cls, condition: str, parameters: list | dict):
        """
        Generates WHERE statement.
        :param condition: Sqlite WHERE condition.
        :param parameters: Query parameters values.
        """
        cls.__statement += f" WHERE {condition}"

        if isinstance(parameters, list):
            cls.__parameters += parameters
        else:
            cls.__parameters = parameters
        return cls()

    @classmethod
    def order_by(cls, column: str):
        """
        Generates ORDER BY statement.
        :param column: Column to order by.
        """
        cls.__statement += f" ORDER BY {column}"
        return cls()

    @classmethod
    def asc(cls):
        """Generates ASC statement."""
        cls.__statement += " ASC"
        return cls()

    @classmethod
    def desc(cls):
        """Generates DESC statement."""
        cls.__statement += " DESC"
        return cls()

    @classmethod
    def limit(cls, __to: int, __from: int = 0):
        """
        Generates LIMIT statement.
        :param __to: Limit of rows to fetch or fetch up to a `number` of rows if `__from` is set.
        :param __from: Number of row to fetch from.
        """
        cls.__statement += f" LIMIT {__to if not __from else f"{__from}, {__to}"}"
        return cls()

    @classmethod
    def build(cls):
        """
        Builds sqlite query.
        :return: :class:`Query`.
        """
        list_of_tuples = any(isinstance(item, tuple) for item in cls.__parameters)
        statement = cls.__statement.strip()
        parameters = cls.__parameters if list_of_tuples or isinstance(cls.__parameters, dict) \
            else tuple(cls.__parameters)
        cls.reset_query()
        return Query(statement=statement, parameters=parameters)

    @classmethod
    def reset_query(cls):
        """Resets all attributes."""
        cls.__statement = cls.__table = None
        cls.__parameters = []
