import os
from sqlite3 import Row
import customtkinter
from src.utils import helpers
import pyperclip
from src.libraries.auth import Auth
from src.models.models import Password
from src.frames.frame_base import FrameBase
from src.mixins.validator_mixin import InputField
from src.libraries.password_manager import PasswordManager
from src.utils import window


class Home(FrameBase):
    def __init__(self, root: PasswordManager, **kwargs):
        super().__init__(root, **kwargs)

        # Images
        self.key_icon = customtkinter.CTkImage(light_image=self.root.images.key)
        self.key_icon_disabled = customtkinter.CTkImage(light_image=self.root.images.key_disabled)
        self.lock_icon = customtkinter.CTkImage(light_image=self.root.images.lock_bw)
        self.unlock_icon = customtkinter.CTkImage(light_image=self.root.images.unlock)

        self.__initialize_gui()

        self.edit_mode: bool = False
        self.passwords = Passwords(self, user_passwords=self.__get_user_passwords())

        # Render passwords list
        self.__render_content()
        self.passwords.lock()
        self.search_input.configure(state=customtkinter.DISABLED)

    def __initialize_gui(self):
        # Link to user settings
        self.settings_btn = customtkinter.CTkButton(
            self,
            width=350,
            height=50,
            image=customtkinter.CTkImage(light_image=self.root.images.settings),
            text=Auth.user.email,
            text_color=self.root.color_mode.primary,
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(17),
            compound="right",
            command=lambda: self.root.show(window.SETTINGS)
        )
        self.settings_btn.place(x=25, y=25)

        # Password form frame
        self.form_frame = customtkinter.CTkFrame(
            self,
            width=350,
            height=590,
            fg_color=self.root.colors.secondary
        )
        self.form_frame.place(x=25, y=85)

        # Account name label
        self.account_name_label = customtkinter.CTkLabel(
            self.form_frame,
            width=330,
            height=30,
            text="  Website/Application:",
            text_color=self.root.colors.primary,
            font=self.root.helvetica(17),
            image=customtkinter.CTkImage(light_image=self.root.images.web),
            compound="left",
            anchor="w"
        )
        self.account_name_label.place(x=10, y=20)

        # Web/App input
        self.web_app_name_input = customtkinter.CTkEntry(
            self.form_frame,
            width=330,
            height=40,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17),
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary
        )
        self.web_app_name_input.place(x=10, y=60)

        # Username label
        self.username_label = customtkinter.CTkLabel(
            self.form_frame,
            width=330,
            height=30,
            text="  Username:",
            text_color=self.root.colors.primary,
            font=self.root.helvetica(17),
            image=customtkinter.CTkImage(light_image=self.root.images.user),
            compound="left",
            anchor="w"
        )
        self.username_label.place(x=10, y=120)

        # Username input
        self.username_input = customtkinter.CTkEntry(
            self.form_frame,
            width=330,
            height=40,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17),
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary
        )
        self.username_input.place(x=10, y=160)

        # Password label
        self.password_label = customtkinter.CTkLabel(
            self.form_frame,
            width=330,
            height=30,
            text="  Password:",
            text_color=self.root.colors.primary,
            font=self.root.helvetica(17),
            image=self.key_icon,
            compound="left",
            anchor="w"
        )
        self.password_label.place(x=10, y=220)

        # Password input
        self.password_input = customtkinter.CTkEntry(
            self.form_frame,
            show="‧",
            width=330,
            height=40,
            text_color=self.root.color_mode.secondary,
            font=self.root.helvetica(17),
            border_color=self.root.colors.primary,
            fg_color=self.root.color_mode.primary
        )
        self.password_input.place(x=10, y=260)
        self.password_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.password_input)
        )

        # Generate password button
        self.generate_btn = customtkinter.CTkButton(
            self.form_frame,
            width=330,
            height=40,
            text="Generate",
            text_color=self.root.color_mode.primary,
            image=customtkinter.CTkImage(light_image=self.root.images.magic_wand),
            compound="right",
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(15),
            command=self.__generate_password
        )
        self.generate_btn.place(x=10, y=310)

        # Add button
        self.add_btn = customtkinter.CTkButton(
            self.form_frame,
            width=330,
            height=40,
            text="Cancel",
            text_color=self.root.color_mode.primary,
            image=customtkinter.CTkImage(light_image=self.root.images.add),
            compound="right",
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(15),
            command=self.__submit_password
        )
        self.add_btn.place(x=10, y=480)
        self.__toggle_add_btn(self.add_btn)

        # Update button
        self.update_btn = customtkinter.CTkButton(
            self.form_frame,
            width=160,
            height=40,
            text="Update",
            text_color=self.root.color_mode.primary,
            image=customtkinter.CTkImage(light_image=self.root.images.refresh),
            compound="right",
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(15),
            command=self.__update_password
        )
        self.update_btn.place(x=10, y=530)
        self.toggle_buttons_state(self.update_btn)

        # Delete button
        self.delete_btn = customtkinter.CTkButton(
            self.form_frame,
            width=160,
            height=40,
            text="Delete",
            text_color=self.root.color_mode.primary,
            image=customtkinter.CTkImage(light_image=self.root.images.bin),
            compound="right",
            fg_color=self.root.colors.disabled,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(15),
            command=self.__delete_password
        )
        self.delete_btn.place(x=180, y=530)
        self.toggle_buttons_state(self.delete_btn)

        # <--- If there is any passwords else show instructions --->
        # Search input
        self.search_input = customtkinter.CTkEntry(
            self,
            width=575,
            height=50,
            border_width=3,
            border_color=self.root.colors.primary,
            font=self.root.helvetica(17),
            fg_color=self.root.color_mode.primary,
            text_color=self.root.color_mode.secondary,
            placeholder_text="Search",
            placeholder_text_color=self.root.colors.disabled
        )
        self.search_input.place(x=400, y=25)
        self.search_input.bind("<KeyRelease>", self.__search_passwords)

        # Scrollable frame
        self.passwords_table_frame = customtkinter.CTkScrollableFrame(
            self,
            width=550,
            height=510,
            fg_color=self.root.colors.secondary
        )
        self.passwords_table_frame.place(x=400, y=85)

        # Pdf button
        self.pdf_btn = customtkinter.CTkButton(
            self,
            width=115,
            height=50,
            text="PDF",
            text_color=self.root.color_mode.primary,
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(17),
            image=customtkinter.CTkImage(light_image=self.root.images.document),
            compound="right",
            command=self.__save_to_pdf
        )
        self.pdf_btn.place(x=400, y=625)

        # User password/passcode input
        self.pass_input = customtkinter.CTkEntry(
            self,
            show="‧",
            width=300,
            height=50,
            text_color=self.root.color_mode.secondary,
            border_color=self.root.colors.primary,
            border_width=3,
            placeholder_text="Enter password",
            placeholder_text_color=self.root.colors.disabled,
            fg_color=self.root.color_mode.primary,
            font=self.root.helvetica(20)
        )
        self.pass_input.place(x=525, y=625)
        self.pass_input.bind(
            "<Double-3>",
            lambda event: self.toggle_password_visibility(self.pass_input)
        )

        # Lock/unlock button
        self.lock_btn = customtkinter.CTkButton(
            self,
            width=137,
            height=50,
            text="Unlock",
            text_color=self.root.color_mode.primary,
            fg_color=self.root.colors.primary,
            hover_color=helpers.adjust_brightness(self.root.colors.primary),
            font=self.root.helvetica(17),
            image=self.unlock_icon,
            compound="right",
            command=self.__lock_btn_click
        )
        self.lock_btn.place(x=835, y=625)

    def __toggle_passwords_table(self):
        if self.passwords.is_locked:
            self.passwords.unlock()
            self.lock_btn.configure(text="Lock", image=self.lock_icon)
        else:
            self.passwords.lock()
            self.lock_btn.configure(text="Unlock", image=self.unlock_icon)

    def __search_passwords(self, _event=None):
        search_param = self.search_input.get()

        if search_param != "":
            self.passwords.hide_table()
            self.passwords.destroy_search_table()
            self.passwords.search = Password.search(
                item=search_param,
                search_in=["account", "username"],
                additional_condition="user_id = :user_id",
                named_params={"user_id": 1}
            )
            self.passwords.show(self.passwords.search_table)
        else:
            self.__render_content()

    def __show_attempts_message(self):
        if Auth.user.attempts > 0:
            msg = (
                f"Wrong password or passcode. "
                f"{Auth.user.attempts} attempt{"s" if Auth.user.attempts > 1 else ""} left."
            )
            level = "warning"
        else:
            msg = "Wrong password or passcode. Password required."
            level = "danger"

        self.root.flash_message(msg, level)

    def __auto_lock(self):
        if Auth.user.lock_timer != -1:
            self.root.after(Auth.user.lock_timer, self.__lock_passwords_table)

    def __unlock_passwords_table(self):
        def unlock():
            Auth.user.reset_attempts()
            self.pass_input.delete(0, customtkinter.END)
            self.__toggle_passwords_table()
            self.search_input.configure(state=customtkinter.NORMAL)
            self.root.flash_message("Passwords unlocked.", "success")
            self.__auto_lock()

        def check_both():
            if passcode == user_input or helpers.verify_password(password, user_input):
                unlock()
            else:
                Auth.user.decrease_attempts()
                self.__show_attempts_message()

        def check_password():
            if helpers.verify_password(password, user_input):
                unlock()
            else:
                self.root.flash_message("Wrong password", "danger")

        result = self.validate({
            "password_or_passcode": InputField(self.pass_input.get(), "required")
        })

        if not result.errors:
            passcode = helpers.decrypt(Auth.user.passcode, os.getenv("CIPHER_KEY")) if Auth.user.passcode else None
            password = helpers.decrypt(Auth.user.password, os.getenv("CIPHER_KEY"))
            user_input = result.passed["password_or_passcode"]
            self.pass_input.configure(border_color=self.root.colors.primary)

            if passcode and Auth.user.attempts > 0:
                check_both()
            else:
                check_password()
        else:
            self.pass_input.configure(border_color=self.root.colors.danger.border)
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __lock_passwords_table(self):
        if not self.passwords.is_locked:
            self.__clear_form()
            self.clear_entries(self.search_input)
            self.search_input.configure(state=customtkinter.DISABLED)
            self.passwords.destroy_search_table()
            self.__render_content()
            self.__toggle_passwords_table()
            self.root.flash_message("Passwords locked.", "success")

    def __lock_btn_click(self):
        state = f"{self.lock_btn.cget("text")}".lower()

        if state == "unlock":
            self.__unlock_passwords_table()
        else:
            self.__lock_passwords_table()

    def __save_to_pdf(self):
        result = self.validate({
            "password": InputField(self.pass_input.get(), "required")
        })

        if not result.errors:
            user_password = helpers.decrypt(Auth.user.password, os.getenv("CIPHER_KEY"))

            if helpers.verify_password(user_password, result.passed["password"]):
                self.pass_input.configure(border_color=self.root.colors.primary)
                self.pass_input.delete(0, customtkinter.END)
                self.root.focus()
                self.__generate_pdf(result.passed["password"])
            else:
                self.root.flash_message("Wrong password.", "danger")
        else:
            self.pass_input.configure(border_color=self.root.colors.danger.border)
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __generate_password(self):
        self.clear_entries(self.password_input)
        self.password_input.insert(0, helpers.generate_password())

    def __render_content(self):
        if self.passwords.user:
            self.enable_buttons(self.pdf_btn, self.lock_btn)
            self.passwords.destroy_search_table()
            self.passwords.show(self.passwords.table)
        else:
            self.disable_buttons(self.pdf_btn, self.lock_btn)

    @staticmethod
    def __get_user_passwords() -> list:
        return Password.find_by(
            "user_id = ?",
            [1, ],
            order_by="id",
            order="DESC"
        ) or []

    def transfer_to_form(self, entry: Row):
        self.__clear_form()
        self.passwords.selected_id = entry["id"]
        self.web_app_name_input.insert(0, entry["account"])
        self.username_input.insert(0, entry["username"])
        self.password_input.insert(0, helpers.decrypt(entry["password"], os.getenv("CIPHER_KEY")))

        if not self.edit_mode:
            self.__toggle_add_btn(self.add_btn)
            self.add_btn.configure(command=self.__cancel_form_edit)
            self.toggle_buttons_state(self.update_btn, self.delete_btn)

        self.edit_mode = True

    def __clear_form(self):
        self.passwords.selected_id = None
        self.clear_entries(self.web_app_name_input, self.username_input, self.password_input)

    def __cancel_form_edit(self):
        self.__clear_form()

        if self.edit_mode:
            self.__toggle_add_btn(self.add_btn)
            self.add_btn.configure(command=self.__submit_password)
            self.toggle_buttons_state(self.update_btn, self.delete_btn)

        self.edit_mode = False

    def __update_passwords_table(self):
        self.__render_content()
        self.__cancel_form_edit()

    def __submit_password(self):
        result = self.validate({
            "web/app": InputField(self.web_app_name_input.get(), "required"),
            "username": InputField(self.username_input.get(), "required"),
            "password": InputField(self.password_input.get(), "required"),
        })

        if not result.errors:
            password = helpers.encrypt(result.passed["password"], os.getenv("CIPHER_KEY"))
            Password.create(
                ("user_id", "account", "username", "password"),
                (1, result.passed["web/app"], result.passed["username"], password)
            )
            self.passwords.add(Password.find_latest())
            self.__update_passwords_table()

            if self.lock_btn.cget("text") == "Unlock":
                self.__lock_passwords_table()

            self.enable_buttons(self.pdf_btn)
            self.__clear_form()
            self.root.flash_message("Entry stored successfully.", "success")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __update_password(self):
        result = self.validate({
            "web/app": InputField(self.web_app_name_input.get(), "required"),
            "username": InputField(self.username_input.get(), "required"),
            "password": InputField(self.password_input.get(), "required")
        })

        if not result.errors:
            if self.confirmation_prompt("Save the changes?"):
                password = helpers.encrypt(result.passed["password"], os.getenv("CIPHER_KEY"))
                Password.update(
                    self.passwords.selected_id,
                    {
                        "account": result.passed["web/app"],
                        "username": result.passed["username"],
                        "password": password
                    }
                )
                self.passwords.update(Password.find_by_id(self.passwords.selected_id))
                self.__update_passwords_table()
                self.root.flash_message("Changes saved successfully", "success")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __delete_password(self):
        if self.confirmation_prompt("Delete the entry?"):
            Password.delete(self.passwords.selected_id)
            self.passwords.delete(self.passwords.selected_id)
            self.__update_passwords_table()

            if not self.passwords.user:
                self.disable_buttons(self.pdf_btn)

            self.root.flash_message("Entry deleted successfully", "success")

    def copy_to_clipboard(self, text):
        def clear_clipboard():
            if pyperclip.paste() == text:
                pyperclip.copy("")

        pyperclip.copy(text)
        self.root.flash_message("Copied to clipboard\nClipboard clears in 15 seconds", "success")
        self.root.after(15000, clear_clipboard)

    def __generate_pdf(self, password: str):
        data = []

        for i, entry in enumerate(self.passwords.user):
            data.append(list(entry[2:]))
            data[i][2] = helpers.decrypt(data[i][2], os.getenv("CIPHER_KEY"))

        data.insert(0, ["Web/App", "Username", "Password"])
        path = self.root.save_file_dialog()

        if path:
            helpers.generate_pdf(
                path, data, "arvydas.bloze28@gmail.com", password
            )
            self.root.flash_message("Document saved successfully.", "success")

    def __toggle_add_btn(self, add_btn_widget):
        if add_btn_widget.cget("text") == "Add":
            add_btn_widget.configure(
                text="Cancel",
                image=customtkinter.CTkImage(light_image=self.root.images.cancel),
            )
        else:
            add_btn_widget.configure(
                text="Add",
                image=customtkinter.CTkImage(light_image=self.root.images.add),
            )


class Passwords:
    def __init__(self, master: Home, user_passwords: list):
        self.master: Home = master
        self.user: list[Row] = user_passwords
        self.__search: list[Row] = []
        self.table: list[dict[str, customtkinter.CTkButton]] = self.__create_rows(self.user)
        self.search_table: list[dict[str, customtkinter.CTkButton]] = []
        self.selected_id = None
        self.is_locked: bool = False
        self.is_hidden: bool = False

    @property
    def search(self):
        return self.__search

    @search.setter
    def search(self, value):
        self.__search = value
        self.search_table = self.__create_rows(self.__search)

    def show(self, table):
        if table is self.table:
            self.is_hidden = False

        for index, row in enumerate(table):
            self.show_row(index, row)

    def destroy_search_table(self):
        for row in self.search_table:
            for widget in row.values():
                widget.destroy()

    def hide_table(self):
        if not self.is_hidden:
            for row in self.table:
                for widget in row.values():
                    widget.grid_forget()

            self.is_hidden = True

    @staticmethod
    def show_row(index, row):
        row["account_btn"].grid(row=index, column=0, padx=5, pady=8)
        row["account_btn"].grid_propagate(False)
        row["password_btn"].grid(row=index, column=1, padx=5, pady=8)
        row["username_btn"].grid(row=index, column=2, padx=5, pady=8)
        row["username_btn"].grid_propagate(False)

    def lock(self):
        self.is_locked = True

        for row in self.table:
            row["password_btn"].configure(image=self.master.key_icon_disabled)

            for widget in row.values():
                widget.configure(state=customtkinter.DISABLED)

    def unlock(self):
        self.is_locked = False

        for row in self.table:
            row["password_btn"].configure(image=self.master.key_icon)

            for widget in row.values():
                widget.configure(state=customtkinter.NORMAL)

    def __create_rows(self, data: list):
        rows = []

        for entry in data:
            rows.append(self.__create_row(entry))

        return rows

    def __create_row(self, entry):
        return {
            "account_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=220,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                text=entry["account"],
                command=lambda e=entry: self.master.transfer_to_form(e),
                state=customtkinter.NORMAL
            ),
            "password_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=60,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                image=self.master.key_icon,
                text="",
                command=lambda e=entry: self.master.copy_to_clipboard(
                    helpers.decrypt(e["password"], os.getenv("CIPHER_KEY"))),
                state=customtkinter.NORMAL
            ),
            "username_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=240,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                text=entry["username"],
                command=lambda e=entry: self.master.copy_to_clipboard(e["username"]),
                state=customtkinter.NORMAL
            )
        }

    def add(self, entry):
        self.user.insert(0, entry)
        self.table.insert(0, self.__create_row(entry))

    def update(self, entry):
        index = self.__find_by_id(entry["id"])
        self.user[index] = entry
        print(self.user[index]["account"])
        self.table[index] = self.__create_row(entry)

    def delete(self, __id):
        index = self.__find_by_id(__id)
        del self.user[index]
        del self.table[index]

    def __find_by_id(self, __id):
        for index, entry in enumerate(self.user):
            if entry["id"] == __id:
                return index
