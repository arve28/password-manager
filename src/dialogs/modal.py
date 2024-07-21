import customtkinter
from src.libraries.password_manager import PasswordManager
from src.utils import helpers


class Modal(customtkinter.CTkToplevel):
    """Top level prompt."""
    def __init__(self, root: PasswordManager, message: str, width: int, height: int, buttons: tuple):
        super().__init__(root)
        self.root = root
        self.message = message
        self.result = None

        # Remove title bar
        self.overrideredirect(True)

        # Set TopLevel widget as modal
        self.grab_set()

        self.title("Prompt")
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

        frame = customtkinter.CTkFrame(
            self,
            width=w + 50,
            height=h + 50,
            fg_color=self.root.color_mode.primary,
            border_width=3,
            border_color=self.root.colors.disabled,
            corner_radius=0
        )
        frame.pack()
        frame.pack_propagate(False)

        label = customtkinter.CTkLabel(
            frame,
            text=message,
            font=root.helvetica(17),
            text_color=self.root.color_mode.secondary
        )
        label.pack(padx=20, pady=20)

        button_frame = customtkinter.CTkFrame(frame, fg_color=self.root.color_mode.primary)
        button_frame.pack(padx=20, pady=(0, 20))

        if not buttons:
            raise Exception(message="Modal requires at least one button")

        for button in buttons:
            btn = self.__button(button_frame, button[0], button[1])
            btn.pack(side=customtkinter.LEFT, padx=5)

        self.attributes("-topmost", True)

    def __button(self, master, text: str, return_value: bool):
        return customtkinter.CTkButton(
            master=master,
            text=text,
            width=100,
            height=40,
            text_color=self.root.color_mode.primary,
            font=self.root.helvetica(17),
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            command=self.__confirm if return_value else self.__cancel
        )

    def __confirm(self):
        self.result = True
        self.__on_close()

    def __cancel(self):
        self.result = False
        self.__on_close()

    def __on_close(self):
        self.grab_release()
        self.destroy()
