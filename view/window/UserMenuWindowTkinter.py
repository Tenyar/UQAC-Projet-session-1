import sys
import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import customtkinter
import pyperclip
from utility import SpinBoxUtility
from PIL import Image
from customtkinter import CTkImage
from utility.ViewFunctionsUtility import hide_window

from utility.ConstantsUtility import (
    DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH
)

MIN_WINDOW_WIDTH = 520
MIN_WINDOW_HEIGHT = 600

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

        self.title("Password Manager [PROTOTYPE]")  # Set title for the main window

        # Default system theme
        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('green')

        # Set window size and behavior
        self.geometry(f"{550}x{600}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create TabView and other UI components
        self.create_window()


    def create_window(self):
        main_frame = customtkinter.CTkFrame(master=self.get_root())
        main_frame.pack(fill="both", expand=True,)
        main_frame.grid_rowconfigure(0, weight=1)  # Center vertically
        main_frame.grid_columnconfigure(0, weight=1)  # Center horizontally

        #   Create a frame for input fields and labels
        sub_frame = customtkinter.CTkFrame(master=main_frame)
        sub_frame.pack(pady=DEFAULT_PADDING_Y, padx=DEFAULT_PADDING_X, expand=True)

        # Add a button at the top of the tab view
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
            cursor="hand2"
        )
        self.button_disconnect.grid(row=0, column=0, sticky="e", padx=(0, DEFAULT_PADDING_Y), pady=(DEFAULT_PADDING_Y, 0))

        # Create the TabView below the button
        self.tabview = customtkinter.CTkTabview(sub_frame, fg_color="gray75", width=500, height=500)
        self.tabview.grid(row=1, column=0, sticky="")

        # Customize tab buttons
        self.tabview._segmented_button.configure(
            font=("Roboto", 16, "bold"),  # Increase font size
            height=50,                   # Increase button height
            corner_radius=10,            # Adjust corner radius
        )

        # Add and configure tabs
        self.tabview.add("PasswordGenerator")
        self.tabview.add("UserMenu")
        self.tabview.add("Chest")

        # Set up each tab
        self.setup_password_generator_tab()
        self.setup_user_menu_tab()
        self.setup_chest_tab()


    def setup_password_generator_tab(self):
        #   Set up the PasswordGenerator tab
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
        self.label_service_name_error.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        self.input_service_name = customtkinter.CTkEntry(
            master=tab, 
            placeholder_text="service name", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_service_name.grid(row=1, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)

        #   Create a read-only entry field
        self.show_generated_password = customtkinter.CTkEntry(
            master=tab, 
            placeholder_text="", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            state="readonly"
            )
        self.show_generated_password.grid(row=2, column=0, sticky="ew", padx=40, pady=(DEFAULT_PADDING_Y, 0))
        self.show_generated_password.insert(0, "Your generated password")
        
        path_icon_refresh = os.path.join(self.base_dir, "../../assets/icon_refresh.png")
        try:
            pil_image = Image.open(path_icon_refresh)
            image_icon_refresh = CTkImage(pil_image, size=(25, 25))
        except Exception as e:
            print(f"Error loading image: {e}")
            image_icon_refresh = None
        self.button_refresh_password = customtkinter.CTkButton(
            master=tab,
            text="",
            width=BUTTON_DEFAULT_WIDTH,
            image=image_icon_refresh,
            cursor="hand2"
        )
        self.button_refresh_password.grid(row=3, column=0, sticky="e", padx=(0, 40), pady=(2, 0))

        path_icon_clipboard = os.path.join(self.base_dir, "../../assets/icon_clipboard.png")
        try:
            pil_image = Image.open(path_icon_clipboard)
            image_icon_clipboard = CTkImage(pil_image, size=(25, 25))
        except Exception as e:
            print(f"Error loading image: {e}")
            image_icon_clipboard = None
        self.button_copy_clipboard = customtkinter.CTkButton(
            master=tab,
            text="",
            width=BUTTON_DEFAULT_WIDTH,
            image=image_icon_clipboard,
            cursor="hand2",
            command=self.copy_to_clipboard
        )
        self.button_copy_clipboard.grid(row=3, column=0, sticky="e", padx=(0, 85), pady=(2, 0))

        password_params_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        password_params_frame.grid(row=4, column=0, padx=40, pady=3, sticky="we")
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

        alphabet_lowercase_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        alphabet_lowercase_frame.grid(row=5, column=0, padx=40, pady=3, sticky="we")
        alphabet_lowercase_frame.grid_columnconfigure(0, weight=1)
        self.alphabet_lowercase_switch = customtkinter.CTkSwitch(
            master=alphabet_lowercase_frame,
            text="",
            width=60,  
            height=25, 
        )
        self.alphabet_lowercase_switch.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        label_lowercase_alphabet = customtkinter.CTkLabel(
            master=alphabet_lowercase_frame,
            text="a-z",
            compound="left",
            font=("Roboto", 18, "bold"),
            anchor="w"
        )
        label_lowercase_alphabet.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=2)

        alphabet_uppercase_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        alphabet_uppercase_frame.grid(row=6, column=0, padx=40, pady=3, sticky="we")
        alphabet_uppercase_frame.grid_columnconfigure(0, weight=1)
        self.alphabet_uppercase_switch = customtkinter.CTkSwitch(
            master=alphabet_uppercase_frame,
            text="",
            width=60,  
            height=25, 
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

        numbers_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        numbers_frame.grid(row=7, column=0, padx=40, pady=2, sticky="we")
        numbers_frame.grid_columnconfigure(0, weight=1)
        self.numbers_switch = customtkinter.CTkSwitch(
            master=numbers_frame,
            text="",
            width=60,  # Adjust the width if necessary
            height=25,  # Adjust the height if necessary
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

        special_chars_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        special_chars_frame.grid(row=8, column=0, padx=40, pady=3, sticky="we")
        special_chars_frame.grid_columnconfigure(0, weight=1)
        self.special_chars_switch = customtkinter.CTkSwitch(
            master=special_chars_frame,
            text="",
            width=60,
            height=25,
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

        minimum_numbers_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        minimum_numbers_frame.grid(row=9, column=0, padx=40, pady=3, sticky="we")
        minimum_numbers_frame.grid_columnconfigure(0, weight=1)
        minimum_numbers_spinbox = SpinBoxUtility.FloatSpinbox(self, width=30, frame=minimum_numbers_frame, step_size=1)
        minimum_numbers_spinbox.set(0)
        label_minimum_numbers = customtkinter.CTkLabel(
            master=minimum_numbers_frame,
            text="numbers in the password",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        label_minimum_numbers.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=3)

        minimum_special_chars_frame = customtkinter.CTkFrame(master=tab, fg_color="#E0D0F0", border_width=1, border_color="#691ABC")
        minimum_special_chars_frame.grid(row=10, column=0, padx=40, pady=3, sticky="we")
        minimum_special_chars_frame.grid_columnconfigure(0, weight=1)
        minimum_special_chars_spinbox = SpinBoxUtility.FloatSpinbox(self, width=30, frame=minimum_special_chars_frame, step_size=1)
        minimum_special_chars_spinbox.set(0)
        label_minimum_special_chars = customtkinter.CTkLabel(
            master=minimum_special_chars_frame,
            text="special characters in the password",
            compound="left",
            font=("Roboto", 16, "bold"),
            anchor="w"
        )
        label_minimum_special_chars.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=3)

        self.button_submit = customtkinter.CTkButton(
            master=tab, 
            text="Submit", 
            width=50,
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black",
            cursor="hand2"
        )
        self.button_submit.grid(row=11, column=0, sticky="", padx=(5, 5), pady=DEFAULT_PADDING_Y)
        

    def setup_user_menu_tab(self):
        """Set up the UserMenu tab"""
        tab = self.tabview.tab("UserMenu")
        tab.grid_columnconfigure(0, weight=1)

        # Add a label for user options
        user_label = customtkinter.CTkLabel(tab, text="User Options:")
        user_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")


    def setup_chest_tab(self):
        """Set up the Chest tab"""
        tab = self.tabview.tab("Chest")
        tab.grid_columnconfigure(0, weight=1)

        # Add a label for stored passwords
        chest_label = customtkinter.CTkLabel(tab, text="Stored Passwords:")
        chest_label.grid(row=0, column=0, pady=10, padx=10, sticky="n")


    def get_root(self):
        return self


    def get_value(self, widget):
        return self.values[widget]


    def get_controller(self):
        return self.controller


    def get_appearance_mode_optionemenu(self):
        return self.appearance_mode_optionemenu


    def copy_to_clipboard(self):
        # Retrieve the text from the read-only entry field
        password = self.show_generated_password.get()
        if password:  # Ensure there is something to copy
            pyperclip.copy(password)
            print("Password copied to clipboard!")


    def clear_error(self, widget):
        if widget == "username_input" and self.input_field_username.cget("border_color") == "red":
            self.label_username_error.configure(text="")
            self.input_field_username.configure(border_color="gray35")
        elif widget == "master_password_input" and self.input_field_password.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_password.configure(border_color="gray35")


    def on_close(self):
        #   Handle window close event.
        self.quit()  # Stops the mainloop
        self.destroy()  # Destroys the window and resources
        self.get_controller().set_running(False)


    def show_error(self, widget, error_msg):
        if widget == "username_input":
            self.label_username_error.configure(text=error_msg)
            self.input_field_username.configure(border_color="red")
        else:
            self.label_password_error.configure(text=error_msg)
            self.input_field_password.configure(border_color="red")


#   ------------ Theme methods ------------------------------
#   Change button colors dynamically based on the theme.
    def change_appearance_mode(self, new_appearance_mode: str):
        # Disable the option menu to block interaction (ensure no interference)
        self.appearance_mode_optionemenu.configure(state="disabled")

        # Hide the window temporarily (prettier)
        hide_window(self)

        # Set the appearance mode globally
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.get_controller().theme_change_all(new_appearance_mode)


    def update_theme(self, colors):
        # Define colors for buttons based on the theme
        BUTTON_TEXT_COLOR = colors["button_text_color"]
        TITLE_FG_COLOR = colors["title_fg_color"]
        # Update button colors dynamically
        self.appearance_mode_optionemenu.configure(text_color=BUTTON_TEXT_COLOR)
        self.title_frame.configure(fg_color=TITLE_FG_COLOR)
        self.button_login.configure(text_color=BUTTON_TEXT_COLOR)
        self.button_sign_in.configure(text_color=BUTTON_TEXT_COLOR)


    def update_slider_label(self, value, label_name, label_widget):
        label_widget.configure(text=f"{label_name} {int(float(value))}")

# Run the application
if __name__ == "__main__":
    app = UserMenuWindowTkinter("tst")
    app.mainloop()