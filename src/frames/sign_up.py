import os
import customtkinter
from src.utils import helpers
from src import style
from src.utils import window
from src.libraries.auth import Credentials, Auth
from src.frames.frame_base import FrameBase
from src.models.models import User
from src.libraries.password_manager import PasswordManager
from src.mixins.validator_mixin import InputField


class SignUp(FrameBase):
    def __init__(self, root: PasswordManager, **kwargs):
        super().__init__(root, **kwargs)
        self.__initialize_gui()

    def __initialize_gui(self):
        # Side image
        self.img_canvas = customtkinter.CTkLabel(
            self,
            text="",
            height=self.root.height,
            width=self.root.width,
            image=customtkinter.CTkImage(
                light_image=self.root.images.sign_up,
                size=(500, 500)),
            fg_color=self.root.theme_colors[style.TURQUOISE].secondary,
            anchor="w"
        )
        self.img_canvas.place(x=0, y=0)

        self.form_frame = customtkinter.CTkFrame(
            self,
            corner_radius=30,
            width=450,
            height=600,
            fg_color=self.root.colors.light,
            bg_color=self.root.theme_colors[style.TURQUOISE].secondary
        )
        self.form_frame.place(x=500, y=50)

        # Welcome label
        self.welcome_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Welcome!",
            font=self.root.helvetica(35),
            text_color=self.root.theme_colors[style.TURQUOISE].primary,
            anchor="w",
            width=350
        )
        self.welcome_label.place(x=50, y=50)

        # Message label
        self.message_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Create your account",
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
            text_color=self.root.theme_colors[style.TURQUOISE].primary,
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
            border_color=self.root.theme_colors[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(15)
        )
        self.email_input.place(x=50, y=190)

        # Password input label
        self.lock_image = customtkinter.CTkImage(
            light_image=self.root.images.load_icon(f"lock_{style.TURQUOISE}"))
        self.password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=self.lock_image,
            text="  Password:",
            font=self.root.helvetica(17),
            text_color=self.root.theme_colors[style.TURQUOISE].primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.password_label.place(x=50, y=250)

        # Password input
        self.password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=350,
            height=40,
            border_color=self.root.theme_colors[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(17)
        )
        self.password_input.place(x=50, y=280)
        self.password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.password_input)
        )

        # Confirm password input label
        self.confirm_password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=self.lock_image,
            text="  Confirm password:",
            font=self.root.helvetica(17),
            text_color=self.root.theme_colors[style.TURQUOISE].primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.confirm_password_label.place(x=50, y=340)

        # Confirm password input
        self.confirm_password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=350,
            height=40,
            border_color=self.root.theme_colors[style.TURQUOISE].primary,
            fg_color=self.root.colors.light,
            text_color=self.root.colors.dark,
            font=self.root.helvetica(17)
        )
        self.confirm_password_input.place(x=50, y=370)
        self.confirm_password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.confirm_password_input)
        )

        # Submit button
        self.submit_btn = customtkinter.CTkButton(
            self.form_frame,
            text="Submit",
            text_color=self.root.colors.light,
            font=self.root.helvetica(15),
            fg_color=self.root.theme_colors[style.TURQUOISE].primary,
            hover_color=helpers.adjust_brightness(
                self.root.theme_colors[style.TURQUOISE].primary),
            width=350,
            height=40,
            command=self.__submit
        )
        self.submit_btn.place(x=50, y=470)

        # Sign in button
        self.sign_in_btn = customtkinter.CTkButton(
            self.form_frame,
            text="Sign in",
            text_color=self.root.theme_colors[style.TURQUOISE].primary,
            font=self.root.helvetica(15),
            fg_color=self.root.theme_colors[style.TURQUOISE].secondary,
            hover_color=helpers.adjust_brightness(
                self.root.theme_colors[style.TURQUOISE].secondary),
            width=350,
            height=40,
            command=lambda: self.root.show(window.LOG_IN)
        )
        self.sign_in_btn.place(x=50, y=520)

    def __submit(self):
        password = self.password_input.get()
        result = self.validate({
            "email": InputField(self.email_input.get(), "required|unique:User"),
            "password": InputField(password, "required"),
            "password_confirmation": InputField(
                self.confirm_password_input.get(),
                f"required|match:{password}"
            ),
        })

        if not result.errors:
            hashed_password = helpers.encrypt(
                helpers.hash_password(result.passed["password"]),
                os.getenv("CIPHER_KEY")
            )
            User.create(
                fields=("email", "password"),
                values=(result.passed["email"], hashed_password)
            )
            Auth.log_in(Credentials(email=result.passed["email"], password=password))
            self.successful_log_in()
            self.root.flash_message("Signed up successfully.", "success")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")
