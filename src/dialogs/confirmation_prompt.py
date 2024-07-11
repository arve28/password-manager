import customtkinter
from src.utils import helpers


class ConfirmationPrompt(customtkinter.CTkToplevel):
    def __init__(self, root, message: str):
        super().__init__(root)
        self.root = root
        self.message = message
        self.result = None
        self.title("Confirmation")
        self.configure(fg_color=self.root.colors.background)
        self.resizable(self.root.is_resizable, self.root.is_resizable)

        # Calculate center position relative to parent window
        parent_width = self.root.winfo_reqwidth()
        parent_height = self.root.winfo_reqheight()
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()

        self_width = 350  # Width of the prompt window
        self_height = 100  # Height of the prompt window
        self_x = parent_x + (parent_width // 2) - (self_width // 2)
        self_y = parent_y + (parent_height // 2) - (self_height // 2)
        self.geometry(f"{self_width}x{self_height}+{self_x+390}+{self_y+190}")

        label = customtkinter.CTkLabel(
            self,
            text=message,
            font=root.helvetica(17),
            text_color=self.root.colors.dark
        )
        label.pack(padx=20, pady=10)

        button_frame = customtkinter.CTkFrame(self, fg_color=self.root.colors.background)
        button_frame.pack(padx=20, pady=(0, 20))

        yes_button = customtkinter.CTkButton(
            button_frame,
            text="Yes",
            text_color=self.root.colors.light,
            font=self.root.helvetica(17),
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            command=self.confirm
        )
        yes_button.pack(side=customtkinter.LEFT, padx=5)

        no_button = customtkinter.CTkButton(
            button_frame,
            text="No",
            text_color=self.root.colors.light,
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
