from sqlite3 import Row
from typing import Optional, List
from src.libraries.database import Database as Db
from src.libraries.table import TableBase


class Model:
    """Base class for the database's table's model."""
    table: Optional[type[TableBase]] = None

    @classmethod
    def find(cls, fields: Optional[dict | tuple] = None, limit: Optional[int] = None,
             order_by: str = "id", order: str = "asc") -> List[Row] | Row:
        """
        Fetches rows from the table. Expected formats:
        :param fields: Columns to retrieve - :class:`TableBase`.selectable.
        :param limit: - Number of rows.
        :param order_by: - Table column.
        :param order: - `asc` (descending) or `desc` (descending).
        :return: List of Row objects or a Row object if the limit is set to 1.
        """
        Db.select(cls.table, fields if fields else cls.table.selectable)

        if cls.table.references:
            Db.left_join(cls.table.references)

        Db.order_by(f"{cls.table.name}.{order_by}")

        if order.upper() == "ASC":
            Db.asc()
        elif order.upper() == "DESC":
            Db.desc()

        if limit:
            Db.limit(limit)

        return Db.get_one() if limit == 1 else Db.get()

    @classmethod
    def find_by_id(cls, __id, fields: Optional[dict | tuple] = None) -> Row:
        """
        Fetches row from the table where ids matches. Expected formats:
        :param __id: Table row's id.
        :param fields: Columns to retrieve - :class:`TableBase`.selectable.
        :return: Row object.
        """
        return (Db.select(cls.table, fields if fields else cls.table.selectable)
                .where(condition=f"{cls.table.name}.id = ?", parameters=[__id,])).get_one()

    @classmethod
    def find_by(cls, condition: str, parameters: list, fields: Optional[dict | tuple] = None,
                limit: Optional[int] = None, order_by: str = "id", order: str = "asc") -> List[Row] | Row:
        """
        Fetches rows from the table according to condition. Expected formats:
        :param condition: - Sqlite condition.
        :param parameters: List of query parameters "?" - (param_value, param_value, ...)
        :param fields: Columns to retrieve - :class:`TableBase`.selectable.
        :param limit: - Number of rows.
        :param order_by: - Table column.
        :param order: - `asc` (descending) or `desc` (descending).
        :return: list of Row objects or a Row object if the limit is set to 1.
        """
        Db.select(cls.table, fields if fields else cls.table.selectable).where(condition, parameters)
        if cls.table.references:
            Db.left_join(cls.table.references)

        Db.order_by(f"{cls.table.name}.{order_by}")

        if order.upper() == "ASC":
            Db.asc()
        elif order.upper() == "DESC":
            Db.desc()

        if limit:
            Db.limit(limit)

        return Db.get_one() if limit == 1 else Db.get()

    @classmethod
    def search(cls, item: str, search_in: list, additional_condition: Optional[str] = None,
               named_params: Optional[dict] = None, fields: Optional[dict | tuple] = None,
               limit: Optional[int] = None, order_by: str = "id", order: str = "asc") -> List[Row] | Row:
        """
        Fetches rows from the table where item matches values in defined table columns. Expected formats:
        :param item: - Search for.
        :param search_in: Columns to search in - ("col", "col", ...).
        :param additional_condition: - Sqlite WHERE condition.
        :param named_params: Named query parameters ":name" - {"name1": value, "name2": value, ...}
        :param fields: Columns to retrieves - :class:`TableBase`.selectable.
        :param limit: - Number of rows.
        :param order_by: - Table column.
        :param order: - `asc` (descending) or `desc` (descending).
        :return: list of Row objects or a Row object if the limit is set to 1.
        """
        condition = (f"{search_in[0] if len(search_in) == 1 else f"{" || ', ' || ".join(search_in)}"}"
                     f" LIKE :search")
        condition = f"{f"{additional_condition} AND {condition}" if additional_condition else condition}"

        if named_params:
            named_params.update({"search": f"%{item}%"})
        else:
            named_params = {"search": f"%{item}%"}

        Db.select(cls.table, fields if fields else cls.table.selectable).where(condition, named_params)

        if cls.table.references:
            Db.left_join(cls.table.references)

        Db.order_by(f"{cls.table.name}.{order_by}")

        if order.upper() == "ASC":
            Db.asc()
        elif order.upper() == "DESC":
            Db.desc()

        if limit:
            Db.limit(limit)

        return Db.get_one() if limit == 1 else Db.get()

    @classmethod
    def create(cls, fields: tuple, values: list | tuple, ignore: bool = False) -> int:
        """
        Creates the row/rows. Expected formats:
        :param fields: Table columns - ("col1", "col2", ...).
        :param values: List of rows or row- [(col1_value, col2_value, ...), ...] or (col1_value, col2_value)
        :param ignore: Ignore if any constraint is violated.
        :return: Number of affected row.
        """
        return Db.insert(cls.table, fields, values, ignore).run()

    @classmethod
    def update(cls, __id: str | int, fields: dict) -> int:
        """
        Updates the row. Expected formats:
        :param __id: - `id` of a row to be updated.
        :param fields: Columns and values - {"col1": value, "col2": value, ...}.
        :return: Number of affected row.
        """
        return Db.update(cls.table, fields).where("id = ?", [__id,]).run()

    @classmethod
    def delete(cls, __id: int | str) -> int:
        """
        Deletes the row.
        :param __id: `id` of a row to be deleted.
        :return: Number of affected row.
        """
        return Db.delete(cls.table).where("id = ?", [__id,]).run()
