from dataclasses import dataclass
from src import style
from src.mixins.query_builder_mixin import DataType
from src.libraries.table import TableBase
from src.utils.helpers import SECOND

# references = (
#   ('foreign_key', 'reference_table', 'reference_column'), ...
# )
# selectable = {
#   "table_name": (column, ...), ...
# } or (column, ...)


@dataclass
class Users(TableBase):
    name = "users"
    fields = {
        "id": DataType.integer(primary_key=True, autoincrement=True),
        "email": DataType.text(null=False),
        "password": DataType.text(null=False),
        "key": DataType.text(null=False),
        "salt": DataType.blob(null=False),
        "theme_color": DataType.text(null=False, default=style.TURQUOISE),
        "color_mode": DataType.text(null=False, default=style.LIGHT),
        "lock_timer": DataType.integer(default=30 * SECOND)
    }


@dataclass
class Passwords(TableBase):
    name = "passwords"
    fields = {
        "id": DataType.integer(primary_key=True, autoincrement=True),
        "user_id": DataType.integer(null=False),
        "account": DataType.text(null=False),
        "username": DataType.blob(null=False),
        "password": DataType.blob(null=False)
    }
