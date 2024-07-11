from dataclasses import dataclass
from typing import Optional
from src.models.models import User as UserModel
from src.utils import helpers
import os


@dataclass
class User:
    id: int
    email: str
    password: str
    passcode: str | None
    attempts = 3
    theme_color: str
    color_mode: str
    lock_timer: int

    def reset_attempts(self):
        self.attempts = 3

    def decrease_attempts(self):
        self.attempts -= 1

    def update(self):
        user = UserModel.find_by_id(self.id)
        self.email = user["email"]
        self.password = user["password"]
        self.passcode = user["passcode"]
        self.theme_color = user["theme_color"]
        self.color_mode = user["color_mode"]
        self.lock_timer = user["lock_timer"]


@dataclass
class Credentials:
    email: str
    password: str


class Auth:
    user: Optional[User] = None

    @classmethod
    def log_in(cls, credentials: Credentials):
        user = UserModel.find_by("email = ?", [credentials.email,], limit=1)

        if user:
            user_password = helpers.decrypt(user["password"], os.getenv("CIPHER_KEY"))
            if helpers.verify_password(user_password, credentials.password):
                cls.user = User(
                    id=user["id"],
                    email=user["email"],
                    passcode=user["passcode"],
                    password=user["password"],
                    theme_color=user["theme_color"],
                    color_mode=user["color_mode"],
                    lock_timer=user["lock_timer"]
                )
                return True
        return False

    @classmethod
    def log_out(cls):
        cls.user = None
