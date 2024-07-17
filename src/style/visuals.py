from dataclasses import dataclass
from src.utils.helpers import resource_path
from PIL import Image, ImageFile

# Color name constants
PURPLE = "purple"
TURQUOISE = "turquoise"
BLUE = "blue"
INDIGO = "indigo"
PINK = "pink"
RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
GREEN = "green"
CYAN = "cyan"
DARK = "dark"
LIGHT = "light"


class Images:
    """Class for managing images in application."""
    def __init__(self, color_theme: str, color_mode):
        self.__color_theme = color_theme
        self.__color_mode = color_mode
        self.icons_path = "assets\\icons\\"
        self.images_path = "assets\\images\\"

        # Dynamic icons
        self.envelope = self.load_icon(f"envelope_{self.__color_theme}")
        self.lock = self.load_icon(f"lock_{self.__color_theme}")
        self.web = self.load_icon(f"web_{self.__color_theme}")
        self.user = self.load_icon(f"user_{self.__color_theme}")
        self.key = self.load_icon(f"key_{self.__color_theme}")
        self.settings = self.load_icon(f"settings_{self.__color_mode}")
        self.magic_wand = self.load_icon(f"magic_wand_{self.__color_mode}")
        self.document = self.load_icon(f"document_{self.__color_mode}")
        self.add = self.load_icon(f"add_{self.__color_mode}")
        self.refresh = self.load_icon(f"refresh_{self.__color_mode}")
        self.bin = self.load_icon(f"bin_{self.__color_mode}")
        self.cancel = self.load_icon(f"cancel_{self.__color_mode}")
        self.unlock = self.load_icon(f"unlock_{self.__color_mode}")
        self.lock_bw = self.load_icon(f"lock_{self.__color_mode}")

        # Static icons
        self.key_disabled = self.load_icon("key_disabled")

        # Dynamic images
        self.user_settings = self.load_image(f"settings_{self.__color_theme}")

        # Static images
        self.log_in = self.load_image("log_in")
        self.sign_up = self.load_image("sign_up")

    def update(self, color_theme=None, color_mode=None):
        """
        Reloads different color images.
        :param color_theme: Name of a color theme.
        :param color_mode: Name of a display mode.
        """
        if color_theme and color_theme != self.__color_theme:
            self.__color_theme = color_theme
            self.envelope = self.load_icon(f"envelope_{color_theme}")
            self.lock = self.load_icon(f"lock_{color_theme}")
            self.web = self.load_icon(f"web_{color_theme}")
            self.user = self.load_icon(f"user_{color_theme}")
            self.key = self.load_icon(f"key_{color_theme}")
            self.user_settings = self.load_image(f"settings_{color_theme}")

        if color_mode and color_mode != self.__color_mode:
            self.__color_mode = color_mode
            self.settings = self.load_icon(f"settings_{color_mode}")
            self.magic_wand = self.load_icon(f"magic_wand_{color_mode}")
            self.document = self.load_icon(f"document_{color_mode}")
            self.add = self.load_icon(f"add_{color_mode}")
            self.refresh = self.load_icon(f"refresh_{color_mode}")
            self.bin = self.load_icon(f"bin_{color_mode}")
            self.cancel = self.load_icon(f"cancel_{color_mode}")
            self.unlock = self.load_icon(f"unlock_{color_mode}")
            self.lock_bw = self.load_icon(f"lock_{color_mode}")

    def load_icon(self, icon_name: str) -> ImageFile:
        """
        Loads image from `self.icons_path` directory.
        :param icon_name: Name of an image file without extension.
        """
        return Image.open(resource_path(f"{self.icons_path}{icon_name}.png"))

    def load_image(self, image_name: str) -> ImageFile:
        """
        Loads image from `self.images_path` directory.
        :param image_name: Name of an image file without extension.
        """
        return Image.open(resource_path(f"{self.images_path}{image_name}.png"))


@dataclass
class ColorSubset:
    """Color set"""
    primary: str
    secondary: str


@dataclass
class MessageLevelColor:
    """Color set for message's level."""
    normal: str
    subtle: str
    border: str


@dataclass
class Colors:
    """Class for managing colors in application."""
    primary: str
    secondary: str
    disabled = "#788081"
    light = "#F8F9FA"
    dark = "#212529"
    danger = MessageLevelColor("#DC3545", "#F8D7DA", "#F1AEB5")
    info = MessageLevelColor("#0DCAF0", "#CFF4FC", "#9EEAF9")
    warning = MessageLevelColor("#FFC107", "#FFF3CD", "#FFE69C")
    success = MessageLevelColor("#16784A", "#D1E7DD", "#A3CFBB")

    def update(self, theme_color: ColorSubset):
        """
        Updates main colors (primary and secondary).
        :param theme_color: Theme color name.
        """
        self.primary = theme_color.primary
        self.secondary = theme_color.secondary
