import customtkinter
from src.utils import helpers
from src.libraries.auth import Credentials, Auth
from src.frames.frame_base import FrameBase
from src.libraries.password_manager import PasswordManager
from src.mixins.validator_mixin import InputField
from src.utils import window
from src import style


class LogIn(FrameBase):
    """"Log in" window."""
    def __init__(self, root: PasswordManager, **kwargs):
        super().__init__(root, **kwargs)
        self.__initialize_gui()

    def __initialize_gui(self):
        """Populates window with widgets."""
        # Side image
        self.img_canvas = customtkinter.CTkLabel(
            self,
            text="",
            height=self.root.HEIGHT,
            width=self.root.WIDTH,
            image=customtkinter.CTkImage(
                light_image=self.root.images.log_in,
                size=(500, 500)),
            fg_color=self.root.THEME_COLORS[style.TURQUOISE].secondary,
            anchor="w"
        )
        self.img_canvas.place(x=0, y=0)

        self.form_frame = customtkinter.CTkFrame(
            self,
            corner_radius=30,
            width=450,
            height=600,
            fg_color=self.root.colors.light,
            bg_color=self.root.THEME_COLORS[style.TURQUOISE].secondary
        )
        self.form_frame.place(x=500, y=50)

        # Welcome label
        self.welcome_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Welcome Back!",
            font=self.root.helvetica(35),
            text_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            anchor="w",
            width=350
        )
        self.welcome_label.place(x=50, y=50)

        # Message label
        self.message_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Sign in to your account",
            font=self.root.helvetica(15),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=350
        )
        self.message_label.place(x=50, y=100)

        # Email input label
        self.email_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.load_icon(f"envelope_{style.TURQUOISE}")),
            text="  Email:",
            font=self.root.helvetica(17),
            text_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.email_label.place(x=50, y=160)

        # Email input
        self.email_input = customtkinter.CTkEntry(
            self.form_frame,
            width=350,
            height=40,
            border_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(15)
        )
        self.email_input.place(x=50, y=190)
        self.email_input.bind("<Return>", self.__log_in)

        # Password input label
        self.password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.load_icon(f"lock_{style.TURQUOISE}")),
            text="  Password:",
            font=self.root.helvetica(17),
            text_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.password_label.place(x=50, y=250)

        # Password input
        self.password_input = customtkinter.CTkEntry(
            self.form_frame,
            show=self.password_placeholder,
            width=350,
            height=40,
            border_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(17)
        )
        self.password_input.place(x=50, y=280)
        self.password_input.bind("<Return>", self.__log_in)
        self.password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.password_input)
        )

        # Key input label
        self.key_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.load_icon(f"key_{style.TURQUOISE}")),
            text="  Key:",
            font=self.root.helvetica(17),
            text_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.key_label.place(x=50, y=340)

        # Key input
        self.key_input = customtkinter.CTkEntry(
            self.form_frame,
            show=self.password_placeholder,
            width=350,
            height=40,
            border_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(17)
        )
        self.key_input.place(x=50, y=370)
        self.key_input.bind("<Return>", self.__log_in)
        self.key_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.key_input)
        )

        # Login button
        self.login_btn = customtkinter.CTkButton(
            self.form_frame,
            text="Login",
            text_color=self.root.colors.light,
            font=self.root.helvetica(15),
            fg_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            hover_color=helpers.adjust_brightness(
                self.root.THEME_COLORS[style.TURQUOISE].primary),
            width=350,
            height=40,
            command=self.__log_in
        )
        self.login_btn.place(x=50, y=470)

        # Sign up button
        self.sign_up_btn = customtkinter.CTkButton(
            self.form_frame,
            text="Sign up",
            text_color=self.root.THEME_COLORS[style.TURQUOISE].primary,
            font=self.root.helvetica(15),
            fg_color=self.root.THEME_COLORS[style.TURQUOISE].secondary,
            hover_color=helpers.adjust_brightness(
                self.root.THEME_COLORS[style.TURQUOISE].secondary),
            width=350,
            height=40,
            command=lambda: self.root.show(window.SIGN_UP)
        )
        self.sign_up_btn.place(x=50, y=520)

    def __log_in(self, _event=None):
        """Logs in user."""
        result = self.validate({
            "email": InputField(self.email_input.get(), "required"),
            "password": InputField(self.password_input.get(), "required"),
            "key": InputField(self.key_input.get(), "required")
        })

        if not result.errors:
            user = result.passed
            if Auth.log_in(Credentials(user["email"], user["password"], user["key"])):
                self.successful_log_in()
            else:
                self.root.flash_message("Wrong credentials.", "danger")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")
