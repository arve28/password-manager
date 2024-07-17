import customtkinter
import pystray
import gc
from tkinter import filedialog
from typing import Dict
from PIL import Image
from src.utils import window
from src.libraries.database import Database as Db
from src.utils.helpers import center_window, SECOND, MINUTE, resource_path
from src import style


class PasswordManager(customtkinter.CTk):
    """Password manager application's class."""
    DB_PATH: str = "data\\password_manager.db"
    HEIGHT: int = 700
    WIDTH: int = 1000

    LOCK_TIMERS: Dict[str, int] = {
        "15 sec": 15 * SECOND,
        "30 sec": 30 * SECOND,
        "45 sec": 45 * SECOND,
        "1 min": MINUTE,
        "3 min": 3 * MINUTE,
        "5 min": 5 * MINUTE,
        "10 min": 10 * MINUTE,
        "15 min": 15 * MINUTE,
        "Never": -1
    }

    THEME_COLORS: Dict[str, style.ColorSubset] = {
        style.PURPLE: style.ColorSubset("#6f42c1", "#E2D9F3"),
        style.TURQUOISE: style.ColorSubset("#20c997", "#D2F4EA"),
        style.BLUE: style.ColorSubset("#0d6efd", "#CFE2FF"),
        style.INDIGO: style.ColorSubset("#6610f2", "#E0CFFC"),
        style.PINK: style.ColorSubset("#d63384", "#F7D6E6"),
        style.RED: style.ColorSubset("#dc3545", "#F8D7DA"),
        style.ORANGE: style.ColorSubset("#fd7e14", "#FFE5D0"),
        style.YELLOW: style.ColorSubset("#ffc107", "#FFF3CD"),
        style.GREEN: style.ColorSubset("#198754", "#D1E7DD"),
        style.CYAN: style.ColorSubset("#0DCAF0", "#CFF4FC"),
    }

    current_theme_color: str = style.TURQUOISE

    colors: style.Colors = style.Colors(
        primary=THEME_COLORS[current_theme_color].primary,
        secondary=THEME_COLORS[current_theme_color].secondary
    )

    COLOR_MODES: Dict[str, style.ColorSubset] = {
        style.DARK: style.ColorSubset(colors.dark, colors.light),
        style.LIGHT: style.ColorSubset(colors.light, colors.dark)
    }

    current_color_mode: str = style.LIGHT
    color_mode: style.ColorSubset = COLOR_MODES[current_color_mode]

    images: style.Images = style.Images(current_theme_color, current_color_mode)

    def __init__(self):
        super().__init__()
        self.is_resizable: bool = False
        self.current_window: str | None = None
        self.windows: dict = {}
        self.__setup()

    def __setup(self):
        """Setups the application."""
        Db.create_connection(resource_path(self.DB_PATH))
        self.load_windows(window.LOG_IN, window.SIGN_UP)
        self.iconbitmap(resource_path("icon.ico"))
        self.title("Password Manager")
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.bind("<Unmap>", self.__on_minimize)
        self.resizable(self.is_resizable, self.is_resizable)
        self.configure(fg_color=self.colors.light)
        customtkinter.set_appearance_mode("system")
        center_window(self, self.WIDTH, self.HEIGHT)

    def run(self):
        """Launch the application."""
        self.show(window.LOG_IN)
        self.mainloop()

    def show(self, window_class_name: str):
        """
        Displays the window.
        :param window_class_name: name of the window class

        """
        if self.current_window:
            self.windows[self.current_window].place_forget()

        self.windows[window_class_name].place(x=0, y=0)
        self.current_window = window_class_name

    def __load_window_class(self, name):
        """
        Loads the window class.
        :param name: name of the window class
        :return: window object
        """
        import src.frames

        # Get the class from the imported module
        window_class = getattr(src.frames, name)
        return window_class(self)

    def refresh_windows(self, *window_class_names):
        """Reinitialize window objects."""
        for window_name in window_class_names:
            self.windows[window_name].destroy()
            del self.windows[window_name]
            self.windows[window_name] = self.__load_window_class(window_name)

            if self.current_window == window_name:
                self.current_window = None

        gc.collect()

    def load_windows(self, *window_class_names):
        """Creates list of window objects."""
        for window_name in window_class_names:
            if window_name not in self.windows:
                self.windows[window_name] = self.__load_window_class(window_name)

    def destroy_windows(self, *window_class_names):
        """Destroys window widgets."""
        for window_name in window_class_names:
            self.windows[window_name].destroy()
            del self.windows[window_name]

            if window_name == self.current_window:
                self.current_window = None

        gc.collect()

    def flash_message(self,  message: str, level: str, duration: int = 3):
        """
        Shows flash message.
        :param message: text to show
        :param level: "danger" - red themed, "success" - green themed or "warning" - yellow themed
        :param duration: time in seconds
        """
        color: style.MessageLevelColor = getattr(self.colors, level)
        message_label = customtkinter.CTkLabel(
            self,
            width=500,
            height=80,
            text=message,
            text_color=color.normal,
            fg_color=color.subtle,
            font=self.helvetica(17)
        )
        message_label.place(x=250, y=0)
        self.after(duration*1000, lambda: message_label.destroy())

    def update_theme(self, theme):
        """
        Updates the application's theme color.
        :param theme: color name from THEME_COLORS
        """
        if theme in self.THEME_COLORS:
            self.current_theme_color = theme
            self.colors.update(self.THEME_COLORS[theme])
            self.images.update(theme)
        else:
            raise KeyError()

    def update_mode(self, mode):
        """
        Updates the application's display mode.
        :param mode: mode name from COLOR_MODES
        """
        if mode in self.COLOR_MODES:
            self.current_color_mode = mode
            self.color_mode = self.COLOR_MODES[mode]
            self.images.update(color_mode=mode)
        else:
            raise KeyError()

    @staticmethod
    def helvetica(size: int, weight: str = "bold") -> tuple:
        """
        Generates tuple with Helvetica font.
        :param size: font size
        :param weight: font weight
        :return: tuple("Helvetica", size, weight)
        """
        return "Helvetica", size, weight

    @staticmethod
    def save_file_dialog():
        """Shows save file dialog."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile="passwords",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save PDF File"
        )
        return file_path or None

    def __on_closing(self):
        """Operations before closing the application."""
        Db.close_connection()
        self.destroy()

    def __on_minimize(self, _event=None):
        """Operations on minimize event."""
        if self.state() == 'iconic':
            self.withdraw()
            self.__create_tray_icon()

    def __create_tray_icon(self):
        """Shows application in system tray."""
        # Function to show the window from the tray
        def show_window(icon, _item):
            self.deiconify()
            icon.stop()

        # Function to exit the application from the tray
        def exit_app(icon, _item):
            self.after(0, _exit_app, icon)

        def _exit_app(icon):
            icon.stop()
            self.__on_closing()

        # Create the system tray icon
        image = Image.open("./assets/icons/lock_turquoise.png")
        menu = pystray.Menu(
            pystray.MenuItem("Open", show_window),
            pystray.MenuItem("Exit", exit_app)
        )
        tray_icon = pystray.Icon("Password Manager", image, "Password Manager", menu)
        tray_icon.run_detached()
