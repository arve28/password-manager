import pyperclip
import customtkinter
from sqlite3 import Row
from src.utils import helpers
from src.libraries.auth import Auth
from src.models.models import Password
from src.frames.frame_base import FrameBase
from src.mixins.validator_mixin import InputField
from src.libraries.password_manager import PasswordManager
from src.utils import window


class Home(FrameBase):
    """"Home" window."""
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
        self.search_input.configure(state=customtkinter.DISABLED)

    def __initialize_gui(self):
        """Populates window with widgets."""
        # Link to user's settings
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
            show=self.password_placeholder,
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

        # Account column label
        self.col_account_label = customtkinter.CTkLabel(
            self.passwords_table_frame,
            text="Web\\App",
            width=240,
            text_color=self.root.colors.primary,
            font=self.root.helvetica(15),
            fg_color="transparent"
        )
        self.col_account_label.grid(row=0, column=0, padx=5, pady=8)

        # Password column label
        self.col_password_label = customtkinter.CTkLabel(
            self.passwords_table_frame,
            text="Password",
            width=60,
            text_color=self.root.colors.primary,
            font=self.root.helvetica(15),
            fg_color="transparent"
        )
        self.col_password_label.grid(row=0, column=1, padx=5, pady=8)

        # Username column label
        self.col_username_label = customtkinter.CTkLabel(
            self.passwords_table_frame,
            text="Username",
            width=220,
            text_color=self.root.colors.primary,
            font=self.root.helvetica(15),
            fg_color="transparent"
        )
        self.col_username_label.grid(row=0, column=2, padx=5, pady=8)

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
            show=self.password_placeholder,
            width=300,
            height=50,
            text_color=self.root.color_mode.secondary,
            border_color=self.root.colors.primary,
            border_width=3,
            placeholder_text="Enter password or passcode",
            placeholder_text_color=self.root.colors.disabled,
            fg_color=self.root.color_mode.primary,
            font=self.root.helvetica(18)
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
        """Toggle accessibility to the passwords table."""
        if self.passwords.is_locked:
            self.passwords.unlock()
            self.lock_btn.configure(text="Lock", image=self.lock_icon)
        else:
            self.passwords.lock()
            self.lock_btn.configure(text="Unlock", image=self.unlock_icon)

    def __search_passwords(self, _event=None):
        """Performs search in user's passwords. Shows results in the table."""
        search_param = self.search_input.get()

        if search_param != "":
            self.passwords.hide_table()
            self.passwords.destroy_search_table()
            self.passwords.search = Password.search(
                item=search_param,
                search_in=["account"],
                additional_condition="user_id = :user_id",
                named_params={"user_id": 1}
            )
            self.passwords.show(self.passwords.search_table)
        else:
            self.__render_content()

    def __auto_lock(self):
        """Denies accessibility to the passwords table, after chosen time period, if a "lock timer" is set."""
        if Auth.user.lock_timer != self.root.LOCK_TIMERS["Never"]:
            self.after(Auth.user.lock_timer, lambda: self.__lock_passwords_table(False))

    def __unlock_passwords_table(self):
        """Grants accessibility to the passwords table."""
        def unlock():
            Auth.user.reset_attempts()
            self.pass_input.delete(0, customtkinter.END)
            self.__toggle_passwords_table()
            self.search_input.configure(state=customtkinter.NORMAL)
            self.root.flash_message("Passwords unlocked.", "success")
            self.__auto_lock()

        def check_password():
            if helpers.verify_password(password, user_input):
                unlock()
            else:
                self.root.flash_message("Wrong password", "danger")

        def check_both():
            if (helpers.verify_password(password, user_input) or
                    helpers.verify_password(passcode, user_input)):
                unlock()
            else:
                Auth.user.decrease_attempts()
                attempts = Auth.user.attempts
                self.root.flash_message(
                    f"Wrong password or passcode.\n"
                    f"{f"Attempts remaining: {attempts}" if attempts > 0 else "Password required."}", "danger")

        result = self.validate({
            "password": InputField(self.pass_input.get(), "required")
        })

        if not result.errors:
            password = Auth.user.password
            passcode = Auth.user.passcode
            user_input = result.passed["password"]
            self.pass_input.configure(border_color=self.root.colors.primary)
            check_both() if Auth.user.passcode and Auth.user.attempts > 0 else check_password()
        else:
            self.pass_input.configure(border_color=self.root.colors.danger.border)
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __lock_passwords_table(self, triggered_by_user: bool = True):
        """Denies accessibility to the passwords table."""
        def lock():
            self.__cancel_form_edit()
            self.clear_entries(self.search_input)
            self.search_input.configure(state=customtkinter.DISABLED)
            self.passwords.destroy_search_table()
            self.__render_content()
            self.__toggle_passwords_table()
            self.root.flash_message("Passwords locked.", "success")

        if not self.passwords.is_locked:
            if not triggered_by_user:
                if self.edit_mode:
                    self.after(30 * helpers.SECOND, lambda: self.__lock_passwords_table(triggered_by_user))
                else:
                    lock()
            else:
                lock()

    def __lock_btn_click(self):
        """`Lock/Unlock` button click command."""
        state = f"{self.lock_btn.cget("text")}".lower()

        if state == "unlock":
            self.__unlock_passwords_table()
        else:
            self.__lock_passwords_table()

    def __save_to_pdf(self):
        """Generates pdf file with user's passwords table."""
        result = self.validate({
            "password": InputField(self.pass_input.get(), "required")
        })

        if not result.errors:
            user_password = Auth.user.password

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
        """Generates random string ant set it as "password" entry value."""
        self.clear_entries(self.password_input)
        self.password_input.insert(0, helpers.generate_password())

    def __render_content(self):
        """Shows user's passwords table."""
        if self.passwords.user:
            self.enable_buttons(self.pdf_btn, self.lock_btn)
            self.passwords.destroy_search_table()
            self.passwords.show(self.passwords.table)
        else:
            self.disable_buttons(self.pdf_btn, self.lock_btn)

    @staticmethod
    def __get_user_passwords() -> list:
        """Retrieves all user's passwords from the database."""
        return Password.find_by(
            "user_id = ?",
            [Auth.user.id, ],
            order_by="id",
            order="DESC"
        ) or []

    def transfer_to_form(self, entry: Row):
        """Sets form's entries values to selected row's values."""
        self.__clear_form()
        self.passwords.selected_id = entry["id"]
        self.web_app_name_input.insert(0, entry["account"])
        self.username_input.insert(0, helpers.decrypt_data(entry["username"], Auth.user.key))
        self.password_input.insert(0, helpers.decrypt_data(entry["password"], Auth.user.key))

        if not self.edit_mode:
            self.__toggle_add_btn(self.add_btn)
            self.add_btn.configure(command=self.__cancel_form_edit)
            self.toggle_buttons_state(self.update_btn, self.delete_btn)

        self.edit_mode = True

    def __clear_form(self):
        """Clears form's entries values."""
        self.passwords.selected_id = None
        self.clear_entries(self.web_app_name_input, self.username_input, self.password_input)

    def __cancel_form_edit(self):
        """Changes form's mode from edit row to add row."""
        self.__clear_form()

        if self.edit_mode:
            self.__toggle_add_btn(self.add_btn)
            self.add_btn.configure(command=self.__submit_password)
            self.toggle_buttons_state(self.update_btn, self.delete_btn)

        self.edit_mode = False

    def __refresh_window(self):
        """Refreshes "Home" window."""
        self.clear_entries(self.search_input)
        self.__render_content()
        self.__cancel_form_edit()

    def __submit_password(self):
        """Creates entry in database and user's passwords list. Refreshes "Home" window on success."""
        result = self.validate({
            "web/app": InputField(self.web_app_name_input.get(), "required"),
            "username": InputField(self.username_input.get(), "required"),
            "password": InputField(self.password_input.get(), "required"),
        })

        if not result.errors:
            entry = result.passed
            username = helpers.encrypt_data(entry["username"], (Auth.user.key, Auth.user.salt))
            password = helpers.encrypt_data(entry["password"], (Auth.user.key, Auth.user.salt))
            Password.create(
                ("user_id", "account", "username", "password"),
                (Auth.user.id, entry["web/app"], username, password)
            )
            self.passwords.add(Password.find_latest())
            self.__refresh_window()

            if self.lock_btn.cget("text") == "Unlock":
                self.__lock_passwords_table()

            self.enable_buttons(self.pdf_btn)
            self.__clear_form()
            self.root.flash_message("Entry stored successfully.", "success")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __update_password(self):
        """Updates entry in database and user's passwords list. Refreshes "Home" window on success."""
        result = self.validate({
            "web/app": InputField(self.web_app_name_input.get(), "required"),
            "username": InputField(self.username_input.get(), "required"),
            "password": InputField(self.password_input.get(), "required")
        })

        if not result.errors:
            entry = result.passed

            if self.show_modal("Save changes?", 300, 130, ("Yes", True), ("No", False)):
                Password.update(
                    self.passwords.selected_id,
                    {
                        "account": entry["web/app"],
                        "username": helpers.encrypt_data(entry["username"], (Auth.user.key, Auth.user.salt)),
                        "password": helpers.encrypt_data(entry["password"], (Auth.user.key, Auth.user.salt))
                    }
                )
                self.passwords.update(Password.find_by_id(self.passwords.selected_id))
                self.__refresh_window()
                self.root.flash_message("Changes saved successfully", "success")
        else:
            self.root.flash_message(next(iter(result.errors.values())), "danger")

    def __delete_password(self):
        """Deletes entry from database and user's passwords list. Refreshes "Home" window on success."""
        if self.show_modal("Delete entry?", 300, 130, ("Yes", True), ("No", False)):
            Password.delete(self.passwords.selected_id)
            self.passwords.delete(self.passwords.selected_id)
            self.__refresh_window()

            if not self.passwords.user:
                self.disable_buttons(self.pdf_btn)

            self.root.flash_message("Entry deleted successfully", "success")

    def copy_to_clipboard(self, text):
        """Copies text to clipboard and clears it after 30 seconds."""
        def clear_clipboard():
            if pyperclip.paste() == text:
                pyperclip.copy("")

        pyperclip.copy(text)
        self.root.flash_message("Copied to clipboard\nClipboard clears in 30 seconds", "success")
        self.root.after(self.root.LOCK_TIMERS["30 sec"], clear_clipboard)

    def __generate_pdf(self, password: str):
        """Generates and saves pdf file with user's passwords table."""
        path = self.root.save_file_dialog()

        if path:
            data_content = []

            for i, entry in enumerate(self.passwords.user):
                data_content.append(list(entry[2:]))
                data_content[i][1] = helpers.decrypt_data(data_content[i][1], Auth.user.key)
                data_content[i][2] = helpers.decrypt_data(data_content[i][2], Auth.user.key)

            data = data_content.copy()
            data.insert(0, ["Web/App", "Username", "Password"])

            helpers.generate_pdf(
                path, data, Auth.user.email, password
            )
            self.root.flash_message("Document saved successfully.", "success")

    def __toggle_add_btn(self, add_btn_widget):
        """Toggles `Add/Cancel` button's appearance."""
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
    """Passwords management class for "Home" window."""
    def __init__(self, master: Home, user_passwords: list):
        self.master: Home = master
        self.is_locked: bool = True
        self.is_hidden: bool = False
        self.user: list[Row] = user_passwords
        self.__search: list[Row] = []
        self.table: list[dict[str, customtkinter.CTkButton]] = self.__create_rows(self.user)
        self.search_table: list[dict[str, customtkinter.CTkButton]] = []
        self.selected_id = None

    @property
    def search(self):
        return self.__search

    @search.setter
    def search(self, value):
        self.__search = value
        self.search_table = self.__create_rows(self.__search)

    def show(self, table):
        """Displays the passwords table content."""
        if table is self.table:
            self.is_hidden = False

        for index, row in enumerate(table):
            self.show_row(index, row)

    def destroy_search_table(self):
        """Destroys all widgets from search results table."""
        for row in self.search_table:
            for widget in row.values():
                widget.destroy()

    def hide_table(self):
        """Hides table with all user's passwords."""
        if not self.is_hidden:
            for row in self.table:
                for widget in row.values():
                    widget.grid_forget()

            self.is_hidden = True

    @staticmethod
    def show_row(index, row):
        """Displays row."""
        index += 1
        row["account_btn"].grid(row=index, column=0, padx=5, pady=8)
        row["account_btn"].grid_propagate(False)
        row["password_btn"].grid(row=index, column=1, padx=5, pady=8)
        row["username_btn"].grid(row=index, column=2, padx=5, pady=8)
        row["username_btn"].grid_propagate(False)

    def lock(self):
        """Sets widgets state to "disabled" in the passwords table."""
        self.is_locked = True

        for row in self.table:
            row["password_btn"].configure(image=self.master.key_icon_disabled)

            for widget in row.values():
                widget.configure(state=customtkinter.DISABLED)

    def unlock(self):
        """Sets widgets state to "normal" in the passwords table."""
        self.is_locked = False

        for row in self.table:
            row["password_btn"].configure(image=self.master.key_icon)

            for widget in row.values():
                widget.configure(state=customtkinter.NORMAL)

    def __create_rows(self, data: list):
        """Creates list of table rows."""
        rows = []

        for entry in data:
            rows.append(self.__create_row(entry))

        return rows

    def __create_row(self, entry):
        """Creates table's row."""
        image = self.master.key_icon_disabled if self.is_locked else self.master.key_icon
        state = customtkinter.DISABLED if self.is_locked else customtkinter.NORMAL
        username = helpers.decrypt_data(entry["username"], Auth.user.key)
        return {
            "account_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=240,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                text=entry["account"],
                command=lambda e=entry: self.master.transfer_to_form(e),
                state=state
            ),
            "password_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=60,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                image=image,
                text="",
                command=lambda e=entry: self.master.copy_to_clipboard(
                    helpers.decrypt_data(e["password"], Auth.user.key)),
                state=state
            ),
            "username_btn": customtkinter.CTkButton(
                self.master.passwords_table_frame,
                height=40,
                width=220,
                font=self.master.root.helvetica(14),
                fg_color=self.master.root.colors.secondary,
                text_color=self.master.root.colors.primary,
                hover_color=helpers.adjust_brightness(self.master.root.colors.secondary),
                text=username,
                command=lambda e=entry: self.master.copy_to_clipboard(username),
                state=state
            )
        }

    def add(self, entry):
        """Adds entry to the user's passwords list and table's row."""
        self.user.insert(0, entry)
        self.table.insert(0, self.__create_row(entry))

    def update(self, entry):
        """Updates entry in the user's passwords list and table's row."""
        index = self.__find_by_id(entry["id"])
        self.user[index] = entry
        self.__destroy_row(self.table, index)
        self.table[index] = self.__create_row(entry)

    def delete(self, __id):
        """Deletes entry from the user's passwords list and table's row."""
        index = self.__find_by_id(__id)
        del self.user[index]
        self.__destroy_row(self.table, index)
        del self.table[index]

    def __find_by_id(self, __id):
        """Gets index of Row object in the user's passwords list where ids matches."""
        for index, entry in enumerate(self.user):
            if entry["id"] == __id:
                return index

    @staticmethod
    def __destroy_row(table: list, index: int):
        """Destroy all widgets in the table's row."""
        for column in table[index].values():
            column.destroy()
