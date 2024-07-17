from abc import ABC
from typing import Optional, Dict


class TableBase(ABC):
    """
    Base class for the database's table.
    :var name: name of the database's table
    :var columns: columns of the table
    :var references: foreign keys - (('foreign_key', 'reference_table', 'reference_column'), ...)
    :var selectable: columns to be selected - {"table_name": (column, ...), ...} or ("column", ...)
    """
    name: Optional[str] = None
    columns: Optional[dict] = None
    references: Optional[tuple[tuple]] = None
    selectable: Dict[str, tuple] | tuple = ("*",)
