from sqlite3 import Row
from src.libraries.model import Model
from src.models import tables


class User(Model):
    """Model to interact with `users` table in database."""
    table = tables.Users


class Password(Model):
    """Model to interact with `passwords` table in database."""
    table = tables.Passwords

    @classmethod
    def find_latest(cls) -> Row:
        return cls.find(limit=1, order_by="id", order="DESC")
