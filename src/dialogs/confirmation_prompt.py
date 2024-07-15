import customtkinter
from src.libraries.password_manager import PasswordManager
from src.utils import helpers


class ConfirmationPrompt(customtkinter.CTkToplevel):
    def __init__(self, root: PasswordManager, message: str, width: int, height: int):
        super().__init__(root)
        self.root = root
        self.message = message
        self.result = None
        self.title("Confirmation")
        self.configure(fg_color=self.root.color_mode.primary)
        self.resizable(self.root.is_resizable, self.root.is_resizable)

        # Calculate center position relative to parent window
        parent_width = self.root.winfo_reqwidth()
        parent_height = self.root.winfo_reqheight()
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()

        w = width  # Width of the prompt window
        h = height  # Height of the prompt window
        self_x = parent_x + (parent_width // 2) - (w // 2)
        self_y = parent_y + (parent_height // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{self_x+390}+{self_y+190}")

        label = customtkinter.CTkLabel(
            self,
            text=message,
            font=root.helvetica(17),
            text_color=self.root.color_mode.secondary,
        )
        label.pack(padx=20, pady=10)

        button_frame = customtkinter.CTkFrame(self, fg_color=self.root.color_mode.primary)
        button_frame.pack(padx=20, pady=(0, 20))

        yes_button = customtkinter.CTkButton(
            button_frame,
            text="Yes",
            width=100,
            text_color=self.root.color_mode.primary,
            font=self.root.helvetica(17),
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            command=self.confirm
        )
        yes_button.pack(side=customtkinter.LEFT, padx=5)

        no_button = customtkinter.CTkButton(
            button_frame,
            text="No",
            width=100,
            text_color=self.root.color_mode.primary,
            font=self.root.helvetica(17),
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            command=self.cancel
        )
        no_button.pack(side=customtkinter.LEFT, padx=5)
        self.attributes("-topmost", True)

    def confirm(self):
        self.result = True
        self.destroy()

    def cancel(self):
        self.result = False
        self.destroy()
