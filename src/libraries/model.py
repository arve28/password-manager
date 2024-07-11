from sqlite3 import Row
from typing import Optional, List
from src.libraries.database import Database as Db
from src.libraries.table import TableBase


class Model:
    table: Optional[type[TableBase]] = None

    @classmethod
    def find(cls, fields: Optional[dict | tuple] = None, limit: Optional[int] = None,
             order_by: str = "id", order: str = "ASC") -> List[Row] | Row:
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
        return (Db.select(cls.table, fields if fields else cls.table.selectable)
                .where(condition=f"{cls.table.name}.id = ?", parameters=[__id,])).get_one()

    @classmethod
    def find_by(cls, condition: str, parameters: list, fields: Optional[dict | tuple] = None,
                limit: Optional[int] = None, order_by: str = "id", order: str = "ASC") -> List[Row] | Row:
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
               limit: Optional[int] = None, order_by: str = "id", order: str = "ASC") -> List[Row] | Row:
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
        return Db.insert(cls.table, fields, values, ignore).run()

    @classmethod
    def update(cls, __id: str | int, fields: dict) -> int:
        return Db.update(cls.table, fields).where("id = ?", [__id,]).run()

    @classmethod
    def delete(cls, __id) -> int:
        return Db.delete(cls.table).where("id = ?", [__id,]).run()
