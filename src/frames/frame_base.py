import customtkinter
from src.utils import window
from src.libraries.auth import Auth
from src.mixins.validator_mixin import ValidatorMixin
from src.dialogs.confirmation_prompt import ConfirmationPrompt
from src.libraries.password_manager import PasswordManager


class FrameBase(customtkinter.CTkFrame, ValidatorMixin):
    def __init__(self, master: PasswordManager, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=master.color_mode.primary,
            width=master.width,
            height=master.height,
            corner_radius=0
        )
        self.root = master

    def disable_buttons(self, *args):
        for widget in args:
            widget.configure(
                state=customtkinter.DISABLED,
                text_color_disabled=self.root.color_mode.primary,
                fg_color=self.root.colors.disabled
            )

    @staticmethod
    def clear_entries(*args):
        for entry in args:
            entry.delete(0, customtkinter.END)

    def enable_buttons(self, *args):
        for widget in args:
            widget.configure(
                state=customtkinter.NORMAL,
                fg_color=self.root.colors.primary
            )

    def toggle_buttons_state(self, *args):
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

    def confirmation_prompt(self, message) -> bool:
        prompt = ConfirmationPrompt(self.root, message)
        self.root.wait_window(prompt)
        return prompt.result

    @staticmethod
    def toggle_password_visibility(entry_widget: customtkinter.CTkEntry):
        if entry_widget.cget("show") == "‧":
            entry_widget.configure(show="")
        else:
            entry_widget.configure(show="‧")

    @staticmethod
    def disable_widgets(*widgets):
        for widget in widgets:
            widget.configure(state=customtkinter.DISABLED)

    @staticmethod
    def enable_widgets(*widgets):
        for widget in widgets:
            widget.configure(state=customtkinter.NORMAL)

    def successful_log_in(self):
        self.root.update_theme(Auth.user.theme_color)
        self.root.update_mode(Auth.user.color_mode)
        self.root.load_windows(window.HOME, window.SETTINGS)
        self.root.destroy_windows(window.LOG_IN, window.SIGN_UP)
        self.root.show(window.HOME)
