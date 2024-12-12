import sys
import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import customtkinter
import pyperclip
from PIL import Image
from customtkinter import CTkImage
from utility.ViewFunctionsUtility import ViewFunctionsUtility
from utility import SpinBoxUtility
from utility.ViewFunctionsUtility import ViewFunctionsUtility
from utility.ConstantsUtility import (
    DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_ENTROPY
)
from functools import partial

MIN_WINDOW_WIDTH = 520
MIN_WINDOW_HEIGHT = 650

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 400
DEFAULT_WIDGET_HEIGHT = 35

TITLE_FONT_SIZE = 24
TITLE_FG_COLOR = "#43d583"

PARAGRAPH_FONT_SIZE = 15
MAIN_PARAGRAPH_PADDING_TOP_Y = 5
MAIN_PARAGRAPH_PADDING_BOTTOM_Y = 20

INPUT_TEXT_PADDING_BOTTOM = 10
INPUT_TEXT_PADDING_TOP= 10

BUTTON_DEFAULT_WIDTH = 30
BUTTON_FONT_SIZE = 18
BUTTON_PADDING_Y = 25
BUTTON_TEXT_COLOR = "Black"
  

class UserMenuWindowTkinter(customtkinter.CTk):
    def __init__(self, controller): 
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.controller = controller
        self.view_utils = ViewFunctionsUtility(controller)

        self.root = customtkinter.CTkToplevel()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.title("Password Manager [PROTOTYPE]")  # Set title for the main window

        self.geometry(f"{525}x{650}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        self.values = {}

        self.create_window()


    def create_window(self):
        main_frame = customtkinter.CTkFrame(master=self.get_root())
        main_frame.pack(fill="both", expand=True,)
        main_frame.grid_rowconfigure(0, weight=1) 
        main_frame.grid_columnconfigure(0, weight=1)  

        title_label = customtkinter.CTkLabel(
            master=main_frame,
            text=f"{self.controller.get_username()} menu",
            font=("Roboto", TITLE_FONT_SIZE)
        )
        title_label.pack(pady=10)

        #   Create a frame for input fields and labels
        sub_frame = customtkinter.CTkFrame(master=main_frame)
        sub_frame.pack(pady=DEFAULT_PADDING_Y, padx=DEFAULT_PADDING_X, expand=False)

        #   Add a button at the top of the tab view
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            master=sub_frame, 
            values=["Light", "Dark"], 
            command=self.change_appearance_mode,
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
            )
        self.appearance_mode_optionemenu.grid(row=0, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 0), pady=(DEFAULT_PADDING_Y, 0))

        self.button_disconnect = customtkinter.CTkButton(
            master=sub_frame,
            text="Disconnect", 
            width=BUTTON_DEFAULT_WIDTH,
            fg_color="#c25364",
            hover_color="#9f4250",
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black",
            command=self.on_close,
            cursor="hand2"
        )
        self.button_disconnect.grid(row=0, column=0, sticky="e", padx=(0, DEFAULT_PADDING_Y), pady=(DEFAULT_PADDING_Y, 0))

        #   Create the TabView below the button
        self.tabview = customtkinter.CTkTabview(sub_frame, width=500)
        self.tabview.grid(row=1, column=0, sticky="")

        #   Customize tab buttons
        self.tabview._segmented_button.configure(
            font=("Roboto", 16, "bold"),  # Increase font size
            height=50,                   # Increase button height
            corner_radius=10            # Adjust corner radius
        )

        #   Add and configure tabs
        self.tabview.add("PasswordGenerator")
        self.tabview.add("UserMenu")
        self.tabview.add("Chest")

        #   Set up each tab
        self.setup_password_generator_tab()
        self.setup_user_menu_tab()
        self.setup_chest_tab()


    def setup_password_generator_tab(self):
        tab = self.tabview.tab("PasswordGenerator")
        tab.grid_columnconfigure(0, weight=1)

        self.label_service_name_error = customtkinter.CTkLabel(
            master=tab,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"
        )
        self.label_service_name_error.grid(row=0, column=0, sticky="w", padx=(40, 0), pady=0)
        self.input_service_name = customtkinter.CTkEntry(
            master=tab,
            placeholder_text="service name", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT
            )
        self.input_service_name.grid(row=1, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)

        #   Create a read-only entry field
        self.input_generated_password = customtkinter.CTkEntry(
            master=tab, 
            placeholder_text="password generated", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            state="readonly"
            )
        self.input_generated_password.grid(row=2, column=0, sticky="ew", padx=40, pady=(5, 0))
        self.input_generated_password.insert(0, "Your generated password")
        
        #   Verify paths
        path_icon_refresh = os.path.abspath(os.path.join(self.base_dir, "../../assets/icon_refresh.png"))
        path_icon_clipboard = os.path.abspath(os.path.join(self.base_dir, "../../assets/icon_clipboard.png"))
       
        try:
            pil_image_refresh = Image.open(path_icon_refresh)
            image_icon_refresh = CTkImage(pil_image_refresh, size=(25, 25))
            self.button_refresh_password = customtkinter.CTkButton(
                master=tab,
                text="",
                width=BUTTON_DEFAULT_WIDTH,
                image=image_icon_refresh,
                command=self.show_password,
                cursor="hand2"
            )
            self.button_refresh_password.grid(row=3, column=0, sticky="e", padx=(0, 40), pady=(2, 0))
        except Exception as e:
            print(f"Error loading image: {e}")
            self.button_refresh_password = customtkinter.CTkButton(
                master=tab,
                text="refresh",
                width=BUTTON_DEFAULT_WIDTH,
                command=self.show_password,
                cursor="hand2"
            )
            self.button_refresh_password.grid(row=3, column=0, sticky="e", padx=(0, 40), pady=(2, 0))

        try:
            pil_image_clipboard = Image.open(path_icon_clipboard)
            image_icon_clipboard = CTkImage(pil_image_clipboard, size=(25, 25))
            self.button_copy_clipboard = customtkinter.CTkButton(
                master=tab,
                text="",
                width=BUTTON_DEFAULT_WIDTH,
                cursor="hand2",
                image=image_icon_clipboard,
                command=lambda: self.copy_to_clipboard(self.input_generated_password)
            )
            self.button_copy_clipboard.grid(row=3, column=0, sticky="e", padx=(0, 85), pady=(2, 0))
        except Exception as e:
            print(f"Error loading image: {e}")
            self.button_copy_clipboard = customtkinter.CTkButton(
                master=tab,
                text="copy",
                width=BUTTON_DEFAULT_WIDTH,
                cursor="hand2",
                command=lambda: self.copy_to_clipboard(self.input_generated_password)
            )
            self.button_copy_clipboard.grid(row=3, column=0, sticky="e", padx=(0, 95), pady=(2, 0))

        self.entropie_progressbar_frame = customtkinter.CTkFrame(tab)
        self.entropie_progressbar_frame.grid(row=4, column=0, padx=40, pady=0, sticky="nsew")
        self.entropie_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.entropie_progressbar_frame.grid_rowconfigure(1, weight=1)
        self.label_entropy = customtkinter.CTkLabel(
            master=self.entropie_progressbar_frame,
            text="Entropy [0]:",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        self.label_entropy.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        self.progressbar_entropy = customtkinter.CTkProgressBar(self.entropie_progressbar_frame)
        self.progressbar_entropy.grid(row=0, column=0, padx=(150, 0), pady=0, sticky="ew")
        self.progressbar_entropy.set(0)

        password_params_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        password_params_frame.grid(row=5, column=0, padx=40, pady=3, sticky="we")
        password_params_frame.grid_columnconfigure(0, weight=1)

        self.slider_password_length = customtkinter.CTkSlider(
            password_params_frame, 
            from_=MIN_PASSWORD_LENGTH, 
            to=MAX_PASSWORD_LENGTH, 
            number_of_steps=(MAX_PASSWORD_LENGTH - MIN_PASSWORD_LENGTH),
            command=lambda value: self.update_slider_label(value, "Password length:", label_password_length)
        )
        self.slider_password_length.grid(row=1, column=0, padx=(5, 5), pady=(0, 5), sticky="we")
        self.slider_password_length.set(DEFAULT_PASSWORD_LENGTH)
        label_password_length = customtkinter.CTkLabel(
            master=password_params_frame,
            text=f"Password length: {DEFAULT_PASSWORD_LENGTH}",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        label_password_length.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(5, 0))

        alphabet_lowercase_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        alphabet_lowercase_frame.grid(row=6, column=0, padx=40, pady=3, sticky="we")
        alphabet_lowercase_frame.grid_columnconfigure(0, weight=1)
        self.alphabet_lowercase_switch = customtkinter.CTkSwitch(
            master=alphabet_lowercase_frame,
            text="",
            width=60,  
            height=25,
            command=self.update_chars_pool
        )
        self.alphabet_lowercase_switch.select()
        self.alphabet_lowercase_switch.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        label_lowercase_alphabet = customtkinter.CTkLabel(
            master=alphabet_lowercase_frame,
            text="a-z",
            compound="left",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        label_lowercase_alphabet.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=2)

        alphabet_uppercase_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        alphabet_uppercase_frame.grid(row=7, column=0, padx=40, pady=3, sticky="we")
        alphabet_uppercase_frame.grid_columnconfigure(0, weight=1)
        self.alphabet_uppercase_switch = customtkinter.CTkSwitch(
            master=alphabet_uppercase_frame,
            text="",
            width=60,  
            height=25,
            command=self.update_chars_pool
        )
        self.alphabet_uppercase_switch.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        label_uppercase_alphabet = customtkinter.CTkLabel(
            master=alphabet_uppercase_frame,
            text="A-Z",
            compound="left",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        label_uppercase_alphabet.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=2)

        numbers_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        numbers_frame.grid(row=8, column=0, padx=40, pady=2, sticky="we")
        numbers_frame.grid_columnconfigure(0, weight=1)
        self.numbers_switch = customtkinter.CTkSwitch(
            master=numbers_frame,
            text="",
            width=60,  # Adjust the width if necessary
            height=25,  # Adjust the height if necessary
            command=self.update_chars_pool
        )
        self.numbers_switch.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        label_numbers = customtkinter.CTkLabel(
            master=numbers_frame,
            text="0-9",
            compound="left",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        label_numbers.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=2)

        special_chars_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        special_chars_frame.grid(row=9, column=0, padx=40, pady=3, sticky="we")
        special_chars_frame.grid_columnconfigure(0, weight=1)
        self.special_chars_switch = customtkinter.CTkSwitch(
            master=special_chars_frame,
            text="",
            width=60,
            height=25,
            command=self.update_chars_pool
        )
        self.special_chars_switch.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        label_special_chars = customtkinter.CTkLabel(
            master=special_chars_frame,
            text="!@#$%^&*",
            compound="left",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        label_special_chars.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=2)

        minimum_numbers_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        minimum_numbers_frame.grid(row=10, column=0, padx=40, pady=3, sticky="we")
        minimum_numbers_frame.grid_columnconfigure(0, weight=1)
        self.minimum_numbers_spinbox = SpinBoxUtility.FloatSpinbox(self, width=30, frame=minimum_numbers_frame, step_size=1)
        self.minimum_numbers_spinbox.set(0)
        label_minimum_numbers = customtkinter.CTkLabel(
            master=minimum_numbers_frame,
            text="numbers in the password",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        label_minimum_numbers.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=3)

        minimum_special_chars_frame = customtkinter.CTkFrame(master=tab, border_width=1, border_color="#691ABC")
        minimum_special_chars_frame.grid(row=11, column=0, padx=40, pady=3, sticky="we")
        minimum_special_chars_frame.grid_columnconfigure(0, weight=1)
        self.minimum_special_chars_spinbox = SpinBoxUtility.FloatSpinbox(self, width=30, frame=minimum_special_chars_frame, step_size=1)
        self.minimum_special_chars_spinbox.set(0)
        label_minimum_special_chars = customtkinter.CTkLabel(
            master=minimum_special_chars_frame,
            text="special characters in the password",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        label_minimum_special_chars.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=3)

        self.button_init = customtkinter.CTkButton(
            master=tab, 
            text="Generate", 
            width=100,
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black",
            command=self.show_password,
            cursor="hand2"
        )
        self.button_init.grid(row=12, column=0, sticky="", padx=(5, 150), pady=(DEFAULT_PADDING_Y, 0))
        self.button_submit = customtkinter.CTkButton(
            master=tab, 
            text="Submit", 
            width=100,
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black",
            command=self.submit_generate_password,
            cursor="hand2",
            state="disabled"  # Initially disabled
        )
        self.button_submit.grid(row=12, column=0, sticky="", padx=(150, 5), pady=(DEFAULT_PADDING_Y, 0))


    def update_chars_pool(self):
        if self.alphabet_uppercase_switch.get() == False and self.numbers_switch.get() == False and self.special_chars_switch.get() == False:
            self.alphabet_lowercase_switch.select()


    def update_entropy(self):
        args = self.get_controller().entropy_verification()
        progress = min(args[1] / MAX_PASSWORD_LENGTH, 1)  #  Ensure value is between 0 and 1
        self.progressbar_entropy.set(progress)
        self.progressbar_entropy.configure(progress_color=args[0])
        self.label_entropy.configure(text=f"Entropy [{args[1]}]:")


    def show_password(self):
        generated_password = self.get_controller().generate_password(self.get_password_values())
        self.values["password"] = generated_password
        if generated_password:
            #   Temporarily make the Entry writable
            self.get_password_widget().configure(state="normal")
            #   Insert the generated password
            self.get_password_widget().delete(0, "end")  #  Clear existing text
            self.get_password_widget().insert(0, generated_password)
            #   Make it read-only again
            self.get_password_widget().configure(state="readonly")
            self.button_submit.configure(state="normal")
            self.update_entropy()


    def submit_generate_password(self):
        self.get_controller().submit_password_to_db(self.get_value("service_name"), self.get_value("password"))
        self.view_utils.os_info_message("[Generating password]", "Password put in DB success")
        self.input_service_name.delete(0, "end")
        self.get_password_widget().configure(state="normal")
        self.input_generated_password.delete(0, "end")
        self.get_password_widget().configure(state="readonly")
        self.fill_chest(self.chest_scrollable_frame)


    def setup_user_menu_tab(self):
        tab = self.tabview.tab("UserMenu")
        tab.grid_columnconfigure(0, weight=1)

        user_label = customtkinter.CTkLabel(tab, text="User Options", font=("Roboto", 18, "bold"))
        user_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.button_delete_account = customtkinter.CTkButton(
            master=tab,
            text="Suppress account", 
            width=BUTTON_DEFAULT_WIDTH,
            fg_color="#c25364",
            hover_color="#9f4250",
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black",
            command=self.suppress_account,
            cursor="hand2"
        )
        self.button_delete_account.grid(row=1, column=0, sticky="", padx=(0, DEFAULT_PADDING_Y), pady=(DEFAULT_PADDING_Y, 0))


    def suppress_account(self):
        self.view_utils.open_ask_password_window("suppress_account", self.get_root())


    def setup_chest_tab(self):
        tab = self.tabview.tab("Chest")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1) 

        chest_label = customtkinter.CTkLabel(tab, text="Stored Passwords", font=("Roboto", 18, "bold"))
        chest_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.chest_scrollable_frame = customtkinter.CTkScrollableFrame(
            master=tab,
            width=400,
            height=375,
            border_width=1,
            border_color="#691ABC",
            corner_radius=10,
        )
        self.chest_scrollable_frame.grid(row=1, column=0, padx=0, pady=3, sticky="nswe")
        self.chest_scrollable_frame.grid_rowconfigure(0, weight=1)
        self.chest_scrollable_frame.grid_columnconfigure(0, weight=1) 
        
        if self.fill_chest(self.chest_scrollable_frame):
            print('success')
        else:
            no_data_label = customtkinter.CTkLabel(self.chest_scrollable_frame, text="No password available", font=("Roboto", 18, "bold"))
            no_data_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")


    def fill_chest(self, frame, msg=None):
        services_passwords = self.get_controller().show_service_password()
        if msg != None:
            print("PASSSWORRDDDSS LEFT  [AFTER DELETE OF SERVICE] : ", services_passwords)
        if services_passwords == None:
            return False

        row_index = 0
        for service in enumerate(services_passwords):
            self.scrollable_frame = customtkinter.CTkScrollableFrame(master=frame, orientation="horizontal", height=50)
            self.scrollable_frame.grid(row=row_index, column=0, padx=0, pady=0, sticky="nsew")
            self.scrollable_frame.grid_columnconfigure(0, weight=1)

            service_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Service: {service[1][0]}", font=("Roboto", 14))
            service_label.grid(row=0, column=0, pady=0, padx=0, sticky="w")

            password_label = customtkinter.CTkLabel(self.scrollable_frame, text=f"[Password]: {service[1][1]}", font=("Roboto", 14, "bold"))
            password_label.grid(row=1, column=0, pady=0, padx=0, sticky="w")
            
            self.button_copy_clipboard = customtkinter.CTkButton(
                master=frame,
                text="Copy password",
                cursor="hand2",
                width=75,
                text_color="black",
                font=("Roboto", 12, "bold"),
                command=partial(self.copy_to_clipboard, password_label)
            )
            self.button_copy_clipboard.grid(row=row_index, column=1, sticky="w", padx=(0, 75), pady=0)
            self.button_delete_password = customtkinter.CTkButton(
                master=frame,
                text="Delete",
                width=75,
                cursor="hand2",
                fg_color="#c25364",
                hover_color="#9f4250",
                text_color="black",
                font=("Roboto", 12, "bold"),
                command=partial(self.suppress_service_password, service_label, password_label)
            )
            self.button_delete_password.grid(row=row_index, column=1, sticky="e", padx=(100, 0), pady=0)
            row_index += 1
        return True


    def suppress_service_password(self, service_name, password):
        args = [self, service_name, password]
        self.view_utils.open_delete_service_confirmation_window(args)


    def get_root(self):
        return self.root


    def get_value(self, widget):
        return self.values[widget]


    def get_password_values(self):
        gen_values = {}
        gen_values["service_name"] = self.input_service_name.get()
        gen_values["generated_password"] = self.input_generated_password.get()
        gen_values["password_length"] = self.slider_password_length.get()
        gen_values["lowercase_alphabet"] = self.alphabet_lowercase_switch.get()
        gen_values["uppercase_alphabet"] = self.alphabet_uppercase_switch.get()
        gen_values["numbers"] = self.numbers_switch.get()
        gen_values["special_chars"] = self.special_chars_switch.get()
        gen_values["min_numbers"] = self.minimum_numbers_spinbox.get()
        gen_values["min_special_chars"] = self.minimum_special_chars_spinbox.get()
        self.values = gen_values
        return gen_values


    def get_password_widget(self):
        return self.input_generated_password


    def get_controller(self):
        return self.controller


    def get_appearance_mode_optionemenu(self):
        return self.appearance_mode_optionemenu


    def copy_to_clipboard(self, widget):
        try:
            # Check if the widget is a CTkLabel or CTkEntry
            if isinstance(widget, customtkinter.CTkLabel):
                password = widget.cget("text")
                cleaned_password = password[len("[Password]: "):].strip()  # Removes the specific text
                pyperclip.copy(cleaned_password)
                print("Password copied to clipboard!")
            elif isinstance(widget, customtkinter.CTkEntry):
                password = widget.get()
                pyperclip.copy(password)
                print("Password copied to clipboard!")
            else:
                raise TypeError("Unsupported widget type")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")


    def on_close(self):
        self.view_utils.open_ask_password_window("on_close")


    def clear_error(self, widget):
        if widget == "service_name_input" and self.input_field_username.cget("border_color") == "red":
            self.label_service_name_error.configure(text="")
            self.input_service_name.configure(border_color="gray35")
        elif widget == "master_password_input" and self.input_field_password.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_password.configure(border_color="gray35")


    def show_error(self, widget, error_msg):
        if widget == "service_name_input":
            self.label_service_name_error.configure(text=error_msg)
            self.input_service_name.configure(border_color="red")


    def update_slider_label(self, value, label_name, label_widget):
        label_widget.configure(text=f"{label_name} {int(float(value))}")
#   ------------ Theme methods ------------------------------
#   Change button colors dynamically based on the theme.
    def change_appearance_mode(self, new_appearance_mode: str):
        # Disable the option menu to block interaction (ensure no interference)
        self.appearance_mode_optionemenu.configure(state="disabled")

        # Hide the window temporarily (prettier)
        self.view_utils.hide_window(self)

        # Set the appearance mode globally
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.get_controller().get_main_controller().theme_change_all(new_appearance_mode)


    def update_theme(self, colors):
        # Define colors for buttons based on the theme
        BUTTON_TEXT_COLOR = colors["button_text_color"]
        # Update button colors dynamically
        self.appearance_mode_optionemenu.configure(text_color=BUTTON_TEXT_COLOR)
        #//self.title_frame.configure(fg_color=TITLE_FG_COLOR)
        self.button_disconnect.configure(text_color=BUTTON_TEXT_COLOR)
        self.button_init.configure(text_color=BUTTON_TEXT_COLOR)
        self.button_submit.configure(text_color=BUTTON_TEXT_COLOR)