import customtkinter
from src.utils import window
from src.libraries.auth import Auth
from src.mixins.validator_mixin import ValidatorMixin
from src.libraries.password_manager import PasswordManager


class FrameBase(customtkinter.CTkFrame, ValidatorMixin):
    """Base class for window."""
    def __init__(self, master: PasswordManager, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=master.color_mode.primary,
            width=master.WIDTH,
            height=master.HEIGHT,
            corner_radius=0
        )
        self.root = master
        self.password_placeholder = "●"

    def disable_buttons(self, *args):
        """Changes widget's state to "disabled" and modifies its appearance."""
        for widget in args:
            widget.configure(
                state=customtkinter.DISABLED,
                text_color_disabled=self.root.color_mode.primary,
                fg_color=self.root.colors.disabled
            )

    @staticmethod
    def clear_entries(*args):
        """Delete content of entries widgets."""
        for entry in args:
            entry.delete(0, customtkinter.END)

    def enable_buttons(self, *args):
        """Changes widget's state to "normal" and modifies its appearance."""
        for widget in args:
            widget.configure(
                state=customtkinter.NORMAL,
                fg_color=self.root.colors.primary
            )

    def toggle_buttons_state(self, *args):
        """Toggle widget's state and appearance."""
        for widget in args:
            if widget.cget("state") == "disabled":
                widget.configure(
                    state=customtkinter.NORMAL,
                    fg_color=self.root.colors.primary
                )
            else:
                widget.configure(
                    state=customtkinter.DISABLED,
                    text_color_disabled=self.root.color_mode.primary,
                    fg_color=self.root.colors.disabled
                )

    def show_modal(self, message, width: int, height: int, *buttons) -> bool:
        """Show top level prompt."""
        from src.dialogs.modal import Modal

        modal = Modal(self.root, message, width, height, buttons)
        self.root.wait_window(modal)
        return modal.result

    def toggle_password_visibility(self, entry_widget: customtkinter.CTkEntry):
        """Toggle entries content between "show" value and actual value."""
        if entry_widget.cget("show") == self.password_placeholder:
            entry_widget.configure(show="")
        else:
            entry_widget.configure(show=self.password_placeholder)

    @staticmethod
    def disable_widgets(*widgets):
        """Changes widget's state to "disabled"."""
        for widget in widgets:
            widget.configure(state=customtkinter.DISABLED)

    @staticmethod
    def enable_widgets(*widgets):
        """Changes widget's state to "normal"."""
        for widget in widgets:
            widget.configure(state=customtkinter.NORMAL)

    def successful_log_in(self):
        """
        Grants access to "Home" and "Settings" windows.
        Sets app's appearance to the user's theme color and mode.
        Shows "Home" window.
        """
        self.root.set_appearance(Auth.user.theme_color, Auth.user.color_mode)
        self.root.load_windows(window.HOME, window.SETTINGS)
        self.root.destroy_windows(window.LOG_IN, window.SIGN_UP)
        self.root.show(window.HOME)
