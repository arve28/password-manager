from dataclasses import dataclass
from typing import Optional
from src.models.models import User as UserModel
from src.utils import helpers


@dataclass
class User:
    id: int
    email: str
    password: str
    key: bytes
    salt: bytes
    theme_color: str
    color_mode: str
    lock_timer: int

    def update(self):
        user = UserModel.find_by_id(self.id)
        self.email = user["email"]
        self.password = user["password"]
        self.theme_color = user["theme_color"]
        self.color_mode = user["color_mode"]
        self.lock_timer = user["lock_timer"]


@dataclass
class Credentials:
    email: str
    password: str
    key: str


class Auth:
    user: Optional[User] = None

    @classmethod
    def log_in(cls, credentials: Credentials):
        user = UserModel.find_by("email = ?", [credentials.email,], limit=1)

        if user:
            if (helpers.verify_password(user["password"], credentials.password)
                    and helpers.verify_password(user["key"], credentials.key)):
                cls.user = User(
                    id=user["id"],
                    email=user["email"],
                    password=user["password"],
                    key=helpers.get_key(credentials.key, user["salt"]),
                    salt=user["salt"],
                    theme_color=user["theme_color"],
                    color_mode=user["color_mode"],
                    lock_timer=user["lock_timer"]
                )
                return True
        return False

    @classmethod
    def log_out(cls):
        cls.user = None
