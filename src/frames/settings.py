import customtkinter
from src.utils.helpers import adjust_brightness, get_key_by_value, verify_password, hash_password
from src.libraries.auth import Auth
from src.frames.frame_base import FrameBase
from src.models.models import User
from src.libraries.password_manager import PasswordManager
from src.mixins.validator_mixin import InputField
from src.utils import window
from src import style


class Settings(FrameBase):
    """"Settings" window."""
    def __init__(self, root: PasswordManager, **kwargs):
        super().__init__(root, **kwargs)
        self.__initialize_gui()

    def __initialize_gui(self):
        """Populates window with widgets."""
        # Side image
        self.img_canvas = customtkinter.CTkLabel(
            self,
            height=self.root.HEIGHT,
            text="",
            width=self.root.WIDTH,
            image=customtkinter.CTkImage(
                light_image=self.root.images.user_settings,
                size=(500, 500)),
            fg_color=self.root.colors.secondary,
            anchor="w"
        )
        self.img_canvas.place(x=0, y=0)

        # Log out button
        self.log_out_btn = customtkinter.CTkButton(
            self,
            text="Log out",
            corner_radius=20,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(15),
            fg_color=self.root.color_mode.primary,
            bg_color=self.root.colors.secondary,
            hover_color=adjust_brightness(
                self.root.colors.primary),
            width=150,
            height=40,
            command=self.__log_out
        )
        self.log_out_btn.place(x=25, y=635)

        self.form_frame = customtkinter.CTkFrame(
            self,
            corner_radius=30,
            width=550,
            height=self.root.HEIGHT,
            fg_color=self.root.color_mode.primary,
            bg_color=self.root.colors.secondary
        )
        self.form_frame.place(x=500, y=0)

        # Welcome label
        self.welcome_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Settings",
            font=self.root.helvetica(35),
            text_color=self.root.colors.primary,
            anchor="w",
            width=350
        )
        self.welcome_label.place(x=50, y=30)

        # Home button
        self.home_btn = customtkinter.CTkButton(
            self.form_frame,
            width=150,
            height=30,
            text="Home",
            font=self.root.helvetica(15),
            text_color=self.root.color_mode.primary,
            fg_color=self.root.colors.primary,
            hover_color=adjust_brightness(self.root.colors.primary),
            command=self.__go_home
        )
        self.home_btn.place(x=300, y=40)

        # Appearance label
        self.appearance_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Appearance",
            font=self.root.helvetica(15),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=350
        )
        self.appearance_label.place(x=50, y=80)

        # Theme color label
        self.theme_color_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Theme color",
            font=self.root.helvetica(13),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=100
        )
        self.theme_color_label.place(x=50, y=115)

        # Option menu for theme color
        self.theme_option_menu = customtkinter.CTkOptionMenu(
            self.form_frame,
            height=35,
            font=self.root.helvetica(14),
            dropdown_font=self.root.helvetica(14),
            values=list(self.root.THEME_COLORS.keys()),
            fg_color=self.root.colors.secondary,
            button_color=self.root.colors.primary,
            text_color=self.root.colors.dark,
            button_hover_color=adjust_brightness(
                self.root.colors.primary),
            dropdown_fg_color=self.root.color_mode.primary,
            dropdown_text_color=self.root.color_mode.secondary,
            dropdown_hover_color=self.root.colors.primary,
            command=self.__switch_theme_color
        )
        self.theme_option_menu.set(Auth.user.theme_color)
        self.theme_option_menu.place(x=50, y=140)

        # Color mode label label
        self.color_mode_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Mode",
            font=self.root.helvetica(13),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=100
        )
        self.color_mode_label.place(x=210, y=115)

        # Color mode switch
        self.color_mode_switch = customtkinter.CTkSwitch(
            self.form_frame,
            height=40,
            switch_height=25,
            switch_width=50,
            text=Auth.user.color_mode.capitalize(),
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(14),
            fg_color=self.root.color_mode.secondary,
            progress_color=self.root.colors.primary,
            button_color=self.root.colors.secondary,
            button_hover_color=adjust_brightness(
                self.root.colors.secondary),
            onvalue=style.LIGHT,
            offvalue=style.DARK,
            command=self.__switch_mode
        )

        if Auth.user.color_mode == style.LIGHT:
            self.color_mode_switch.select()

        self.color_mode_switch.place(x=210, y=140)

        # Lock timer label
        self.lock_timer_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Lock timer",
            font=self.root.helvetica(13),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=50
        )
        self.lock_timer_label.place(x=320, y=115)

        # Option menu for lock timer
        self.lock_timer_option_menu = customtkinter.CTkOptionMenu(
            self.form_frame,
            height=35,
            width=130,
            font=self.root.helvetica(14),
            dropdown_font=self.root.helvetica(14),
            values=list(self.root.LOCK_TIMERS.keys()),
            fg_color=self.root.colors.secondary,
            button_color=self.root.colors.primary,
            text_color=self.root.colors.dark,
            button_hover_color=adjust_brightness(
                self.root.colors.primary),
            dropdown_fg_color=self.root.color_mode.primary,
            dropdown_text_color=self.root.color_mode.secondary,
            dropdown_hover_color=self.root.colors.primary
        )
        self.lock_timer_option_menu.set(
            get_key_by_value(self.root.LOCK_TIMERS, Auth.user.lock_timer)
        )
        self.lock_timer_option_menu.place(x=320, y=140)

        # Profile label
        self.profile_label = customtkinter.CTkLabel(
            self.form_frame,
            text="Profile",
            font=self.root.helvetica(15),
            text_color=self.root.colors.disabled,
            anchor="w",
            width=350
        )
        self.profile_label.place(x=50, y=190)

        # Email input label
        self.email_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.envelope),
            text="  Email:",
            font=self.root.helvetica(17),
            text_color=self.root.colors.primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.email_label.place(x=50, y=230)

        # Email input
        self.email_input = customtkinter.CTkEntry(
            self.form_frame,
            width=350,
            height=40,
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(15),
        )
        self.email_input.insert(0, Auth.user.email)
        self.email_input.place(x=50, y=260)

        # New password input label
        self.new_password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.lock),
            text="  New password:",
            font=self.root.helvetica(17),
            text_color=self.root.colors.primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.new_password_label.place(x=50, y=310)

        # New password input
        self.new_password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=350,
            height=40,
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17)
        )
        self.new_password_input.place(x=50, y=340)
        self.new_password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.new_password_input)
        )

        # Confirm new password input label
        self.confirm_new_password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.lock),
            text="  Confirm new password:",
            font=self.root.helvetica(17),
            text_color=self.root.colors.primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.confirm_new_password_label.place(x=50, y=390)

        # Confirm new password input
        self.confirm_new_password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=350,
            height=40,
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17)
        )
        self.confirm_new_password_input.place(x=50, y=420)
        self.confirm_new_password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.confirm_new_password_input)
        )

        # Current password input label
        self.current_password_label = customtkinter.CTkLabel(
            self.form_frame,
            image=customtkinter.CTkImage(
                light_image=self.root.images.key),
            text="  Current password:",
            font=self.root.helvetica(17),
            text_color=self.root.colors.primary,
            compound="left",
            anchor="w",
            width=350
        )
        self.current_password_label.place(x=50, y=550)

        # Password input
        self.current_password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=350,
            height=40,
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17)
        )
        self.current_password_input.place(x=50, y=580)
        self.current_password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.current_password_input)
        )

        # Save button
        self.save_btn = customtkinter.CTkButton(
            self.form_frame,
            text="Save changes",
            text_color=self.root.color_mode.primary,
            font=self.root.helvetica(15),
            fg_color=self.root.colors.primary,
            hover_color=adjust_brightness(
                self.root.colors.primary),
            width=350,
            height=40,
            command=self.__update_details
        )
        self.save_btn.place(x=50, y=630)

    def __switch_theme_color(self, _event):
        """Updates user's theme color."""
        choice = self.theme_option_menu.get()
        User.update(Auth.user.id, {"theme_color": choice})
        Auth.user.update()
        self.root.update_theme(choice)
        self.__refresh_theme_color()
        self.root.refresh_windows(window.HOME)

    def __go_home(self):
        """Redirects to "Home" window."""
        self.clear_entries(self.email_input)
        self.email_input.insert(0, Auth.user.email)
        self.lock_timer_option_menu.set(
            get_key_by_value(self.root.LOCK_TIMERS, Auth.user.lock_timer)
        )
        self.root.show(window.HOME)

    def __switch_mode(self):
        """Updates user's display mode (`dark/light`)."""
        choice = self.color_mode_switch.get()
        User.update(Auth.user.id, {"color_mode": choice})
        Auth.user.update()
        self.root.update_mode(choice)
        self.__refresh_color_mode()
        self.root.refresh_windows(window.HOME)

    def __log_out(self):
        """Logs out user."""
        Auth.log_out()
        self.root.load_windows(window.LOG_IN, window.SIGN_UP)
        self.root.destroy_windows(window.HOME, window.SETTINGS)
        self.root.show(window.LOG_IN)

    def __refresh_color_mode(self):
        """Refreshes the display mode of "Settings" window."""
        self.log_out_btn.configure(
            text_color=self.root.color_mode.secondary,
            fg_color=self.root.color_mode.primary,
        )

        self.form_frame.configure(
            fg_color=self.root.color_mode.primary
        )

        self.home_btn.configure(
            text_color=self.root.color_mode.primary
        )

        self.theme_option_menu.configure(
            dropdown_fg_color=self.root.color_mode.primary,
            dropdown_text_color=self.root.color_mode.secondary
        )
        self.theme_option_menu.set(Auth.user.theme_color)

        self.color_mode_switch.configure(
            text=Auth.user.color_mode.capitalize(),
            text_color=self.root.color_mode.secondary,
            fg_color=self.root.color_mode.secondary
        )

        if Auth.user.color_mode == style.LIGHT:
            self.color_mode_switch.select()

        self.lock_timer_option_menu.configure(
            dropdown_fg_color=self.root.color_mode.primary,
            dropdown_text_color=self.root.color_mode.secondary
        )

        self.email_input.configure(
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary
        )

        self.new_password_input.configure(
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary
        )

        self.confirm_new_password_input.configure(
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary
        )

        self.current_password_input.configure(
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary
        )

        self.save_btn.configure(
            text_color=self.root.color_mode.primary
        )

    def __refresh_theme_color(self):
        """Refreshes the theme color of "Settings" window."""
        self.img_canvas.configure(
            image=customtkinter.CTkImage(
                light_image=self.root.images.user_settings,
                size=(500, 500)),
            fg_color=self.root.colors.secondary
        )

        self.log_out_btn.configure(
            bg_color=self.root.colors.secondary,
            hover_color=adjust_brightness(
                self.root.colors.primary)
        )

        self.form_frame.configure(
            bg_color=self.root.colors.secondary
        )

        self.welcome_label.configure(
            text_color=self.root.colors.primary
        )

        self.home_btn.configure(
            fg_color=self.root.colors.primary,
            hover_color=adjust_brightness(self.root.colors.primary)
        )

        self.theme_option_menu.configure(
            fg_color=self.root.colors.secondary,
            button_color=self.root.colors.primary,
            text_color=self.root.colors.dark,
            button_hover_color=adjust_brightness(
                self.root.colors.primary),
            dropdown_hover_color=self.root.colors.primary
        )
        self.theme_option_menu.set(Auth.user.theme_color)

        self.color_mode_switch.configure(
            progress_color=self.root.colors.primary,
            button_color=self.root.colors.secondary,
            button_hover_color=adjust_brightness(
                self.root.colors.secondary)
        )

        self.lock_timer_option_menu.configure(
            fg_color=self.root.colors.secondary,
            button_color=self.root.colors.primary,
            text_color=self.root.colors.dark,
            button_hover_color=adjust_brightness(
                self.root.colors.primary),
            dropdown_hover_color=self.root.colors.primary
        )

        self.email_label.configure(
            image=customtkinter.CTkImage(
                light_image=self.root.images.envelope),
            text_color=self.root.colors.primary,
        )

        self.email_input.configure(
            border_color=self.root.colors.primary
        )

        self.new_password_label.configure(
            image=customtkinter.CTkImage(
                light_image=self.root.images.lock),
            text_color=self.root.colors.primary
        )

        self.new_password_input.configure(
            border_color=self.root.colors.primary
        )

        self.confirm_new_password_label.configure(
            image=customtkinter.CTkImage(
                light_image=self.root.images.lock),
            text_color=self.root.colors.primary
        )

        self.confirm_new_password_input.configure(
            border_color=self.root.colors.primary
        )

        self.current_password_label.configure(
            image=customtkinter.CTkImage(
                light_image=self.root.images.key),
            text_color=self.root.colors.primary
        )

        self.current_password_input.configure(
            border_color=self.root.colors.primary
        )

        self.save_btn.configure(
            fg_color=self.root.colors.primary,
            hover_color=adjust_brightness(
                self.root.colors.primary)
        )

    def __update_details(self):
        """Updates user's details."""
        new_password = self.new_password_input.get()
        email = self.email_input.get()
        current_password = self.current_password_input.get()
        results = self.validate({
            "current_password": InputField(current_password, "required"),
            "email": InputField(email, "required" if email == Auth.user.email else "required|unique:User"),
            "new_password": InputField(new_password, "min:8"),
            "new_password_confirmation": InputField(
                self.confirm_new_password_input.get(),
                f"match:{new_password}")
        })

        if not results.errors:
            if verify_password(Auth.user.password, current_password):
                cleaned_data = self.__prepare_data(results.passed)

                if cleaned_data:
                    User.update(Auth.user.id, cleaned_data)
                    Auth.user.update()
                    self.root.refresh_windows(window.HOME, window.SETTINGS)
                    self.root.show(window.SETTINGS)
                    self.root.flash_message("User details updated successfully.", "success")
            else:
                self.root.flash_message("Wrong password", "danger")
        else:
            self.root.flash_message(next(iter(results.errors.values())), "danger")

    def __prepare_data(self, data):
        """Prepares details data to be updated."""
        new_password = hash_password(data["new_password"]) if data["new_password"] else None

        lock_timer = self.root.LOCK_TIMERS[self.lock_timer_option_menu.get()]
        data_to_update = {
            "email": data["email"] if data["email"] != Auth.user.email else None,
            "password": new_password,
            "lock_timer": lock_timer if lock_timer != Auth.user.lock_timer else None
        }
        return {field: value for field, value in data_to_update.items() if value is not None}
