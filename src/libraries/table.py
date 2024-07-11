from abc import ABC
from typing import Optional, Dict


class TableBase(ABC):
    name: Optional[str] = None
    fields: Optional[dict] = None
    references: Optional[tuple[tuple]] = None
    selectable: Dict[str, tuple] | tuple = ("*",)
