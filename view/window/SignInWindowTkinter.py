import os
import customtkinter
from utility.ViewFunctionsUtility import ViewFunctionsUtility

MIN_WINDOW_WIDTH = 775
MIN_WINDOW_HEIGHT = 375

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 500
DEFAULT_WIDGET_HEIGHT = 35

TITLE_FONT_SIZE = 24

PARAGRAPH_FONT_SIZE = 16
MAIN_PARAGRAPH_PADDING_TOP_Y = 10
MAIN_PARAGRAPH_PADDING_BOTTOM_Y = 20

INPUT_TEXT_PADDING_TOP= 10
INPUT_TEXT_PADDING_BOTTOM = 10

BUTTON_FONT_SIZE = 18
BUTTON_PADDING_Y=25
#   ----    Utility constants
from utility.ConstantsUtility import (
    MIN_TIME_COST, MAX_TIME_COST
)

from utility.ConstantsUtility import (
    MIN_MEMORY_COST, MAX_MEMORY_COST
)

from utility.ConstantsUtility import (
    MIN_PARALLELISM, MAX_PARALLELISM
)

from utility.ConstantsUtility import (
    MIN_HASH_LEN, MAX_HASH_LEN
)

from utility.ConstantsUtility import (
    MIN_SALT_LEN, MAX_SALT_LEN
)


class SignInWindowTkinter(customtkinter.CTk):
    def __init__(self, controller):
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.controller = controller
        self.root = customtkinter.CTkToplevel()
        self.root.title("Sign in [PROTOTYPE]")
        self.view_utils = ViewFunctionsUtility(self)

        # //  Ensure the window is on top and grabs focus
       # //self.root.attributes("-topmost", False)
       # //self.root.focus_force()

        #   Set up window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        #   Window size
        self.root.geometry(f"{750}x{375}")
        #   Set minimum size for the window
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        #   Values stored
        self.values = {}

        self.create_window()


    def create_window(self):
        #   Using a tkinter Frame for a background without rounded corners
        self.title_frame = customtkinter.CTkFrame(master=self.get_root(), fg_color="#43d583", border_width=None, corner_radius=0)
        self.title_frame.pack(fill="both", expand=False)  # Takes full width with vertical padding
        #   Title label placed in tkinter frame
        title_label = customtkinter.CTkLabel(
            master=self.title_frame,
            text="Sign in",
            font=("Roboto", TITLE_FONT_SIZE)
        )
        title_label.pack(pady=10)  # Spacing around text

        #   --------- User input side ---------
        #   Main frame with margins to center the content
        main_frame = customtkinter.CTkFrame(master=self.get_root())
        main_frame.pack(fill="both", expand=True,)
        main_frame.grid_rowconfigure(0, weight=1)  # Center vertically
        main_frame.grid_columnconfigure(0, weight=1)  # Center horizontally
        #   Create a frame for input fields and labels
        input_label_frame = customtkinter.CTkFrame(master=main_frame)
        #//input_label_frame.pack(pady=DEFAULT_PADDING_Y, padx=DEFAULT_PADDING_X, expand=True)
        input_label_frame.grid(row=0, column=0, padx=(0,200), sticky="")

        #   Row 0: Text paragraph
        paragraph_text = (
            "Please answer the following"
        )
        #  Automatically adjust text width
        paragraph_label = customtkinter.CTkLabel(
            master=input_label_frame,
            text=paragraph_text,
            font=("Roboto", PARAGRAPH_FONT_SIZE),
            wraplength=DEFAULT_WIDGET_WIDTH  # Limits the width of the text so that it displays on multiple lines
        )
        paragraph_label.grid(row=0, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=(MAIN_PARAGRAPH_PADDING_TOP_Y, 0))
        #   Row 1: Username error label
        self.label_username_error = customtkinter.CTkLabel(
            master=input_label_frame,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"  # Align to the left
        )
        self.label_username_error.grid(row=1, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 2: Username input
        self.input_field_username = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Username", 
            width=DEFAULT_WIDGET_WIDTH,
            height=DEFAULT_WIDGET_HEIGHT
            )
        self.input_field_username.grid(row=2, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 3: Master password error label
        self.label_password_error = customtkinter.CTkLabel(
            master=input_label_frame,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"  # Align to the left
        )
        self.label_password_error.grid(row=3, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 4: Master password input
        self.input_field_password= customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_field_password.grid(row=4, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 5: Label with text
        label_info = customtkinter.CTkLabel(
            master=input_label_frame,
            text="  The master password should be remembered by the user!",
            compound="left",
            font=("Roboto", 12),
            anchor="w"  # Align to the left
        )
        label_info.grid(row=5, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))
        #   Row 6: Ask master password input again for confirmation
        self.input_field_password_confirmation = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password again", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_field_password_confirmation.grid(row=6, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=(0, 20))        
        #   Define a grid(Frame)
        #//input_label_frame.grid_columnconfigure(0, weight=1)
        #   Row 7: Buttons / Submit buttons
        self.button_cancel = customtkinter.CTkButton(
            master=input_label_frame,
            text="Cancel", 
            command=self.on_close,
            width=(self.input_field_username.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_cancel.grid(row=7, column=0, sticky="w", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))
        self.button_submit = customtkinter.CTkButton(
            master=input_label_frame, 
            text="Submit", 
            command=self.submit,
            width=(self.input_field_username.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_submit.grid(row=7, column=0, sticky="e", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))

        #   --------- Master password hashing parameters side ---------
        hash_password_frame = customtkinter.CTkFrame(master=main_frame)
        hash_password_frame.grid(row=0, column=0, padx=(550,0), sticky="")

        label_warning_section = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[Advanced parameters]\n knowingly touch the params!",
            compound="left",
            font=("Roboto", 15, "bold"),
            anchor="w"
        )
        label_warning_section.grid(row=1, column=0, sticky="we", padx=(DEFAULT_PADDING_X, 5), pady=0)

        label_section_name = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="Password hashing parameters",
            compound="left",
            font=("Roboto", 15, "underline"),
            anchor="w"
        )
        label_section_name.grid(row=2, column=0, sticky="we", padx=(DEFAULT_PADDING_X, 5), pady=0)
       
        self.slider_time_cost = customtkinter.CTkSlider(
            hash_password_frame, 
            from_=MIN_TIME_COST, 
            to=MAX_TIME_COST, 
            number_of_steps=(MAX_TIME_COST - MIN_TIME_COST),
            command=lambda value: self.update_slider_label(value, "Time cost:", label_timecost, MAX_TIME_COST, label_timecost_info)
        )
        self.slider_time_cost.grid(row=4, column=0, padx=DEFAULT_PADDING_X, pady=0, sticky="w")
        #   Set the slider to the default value
        self.slider_time_cost.set(MAX_TIME_COST)
        label_timecost = customtkinter.CTkLabel(
            master=hash_password_frame,
            text=f"Time cost: {MAX_TIME_COST}",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_timecost.grid(row=3, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 5), pady=(INPUT_TEXT_PADDING_TOP, 0))
        label_timecost_info = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[DEFAULT]",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_timecost_info.grid(row=3, column=0, sticky="w", padx=(100, 5), pady=(INPUT_TEXT_PADDING_TOP, 0))
                
        self.slider_memory_cost = customtkinter.CTkSlider(
            hash_password_frame, 
            from_=MIN_MEMORY_COST, 
            to=MAX_MEMORY_COST, 
            number_of_steps=(MAX_MEMORY_COST - MIN_MEMORY_COST),
            command=lambda value: self.update_slider_label(value, "Memory cost:", label_memorycost, MAX_MEMORY_COST, label_memorycost_info)
        )
        self.slider_memory_cost.grid(row=6, column=0, padx=DEFAULT_PADDING_X, pady=0, sticky="w")
        self.slider_memory_cost.set(MAX_MEMORY_COST)
        label_memorycost = customtkinter.CTkLabel(
            master=hash_password_frame,
            text=f"Memory cost: {MAX_MEMORY_COST}",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_memorycost.grid(row=5, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 5), pady=0)
        label_memorycost_info = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[DEFAULT]",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_memorycost_info.grid(row=5, column=0, sticky="w", padx=(150, 5), pady=0)

        self.slider_parallelism = customtkinter.CTkSlider(
            hash_password_frame, 
            from_=MIN_PARALLELISM, 
            to=MAX_PARALLELISM, 
            number_of_steps=(MAX_PARALLELISM - MIN_PARALLELISM),
            command=lambda value: self.update_slider_label(value, "Parallelism:", label_parallelism, MAX_PARALLELISM, label_parallelism_info)
        )
        self.slider_parallelism.grid(row=8, column=0, padx=DEFAULT_PADDING_X, pady=0, sticky="w")
        self.slider_parallelism.set(MAX_PARALLELISM)
        label_parallelism = customtkinter.CTkLabel(
            master=hash_password_frame,
            text=f"Parallelism: {MAX_PARALLELISM}",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_parallelism.grid(row=7, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 5), pady=0)
        label_parallelism_info = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[DEFAULT]",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_parallelism_info.grid(row=7, column=0, sticky="w", padx=(110, 5), pady=0)

        self.slider_hash_len = customtkinter.CTkSlider(
            hash_password_frame, 
            from_=MIN_HASH_LEN, 
            to=MAX_HASH_LEN, 
            number_of_steps=(MAX_HASH_LEN - MIN_HASH_LEN),
            command=lambda value: self.update_slider_label(value, "Hash length:", label_hash_len, MAX_HASH_LEN, label_hash_len_info)
        )
        self.slider_hash_len.grid(row=10, column=0, padx=DEFAULT_PADDING_X, pady=0, sticky="w")
        self.slider_hash_len.set(MAX_HASH_LEN)
        label_hash_len = customtkinter.CTkLabel(
            master=hash_password_frame,
            text=f"Hash length: {MAX_HASH_LEN}",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_hash_len.grid(row=9, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 5), pady=0)
        label_hash_len_info = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[DEFAULT]",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_hash_len_info.grid(row=9, column=0, sticky="w", padx=(110, 5), pady=0)

        self.slider_salt_len = customtkinter.CTkSlider(
            hash_password_frame, 
            from_=MIN_SALT_LEN, 
            to=MAX_SALT_LEN, 
            number_of_steps=(MAX_SALT_LEN - MIN_SALT_LEN),
            command=lambda value: self.update_slider_label(value, "Salt length:",label_salt_len, MAX_SALT_LEN, label_salt_len_info)
        )
        self.slider_salt_len.grid(row=12, column=0, padx=DEFAULT_PADDING_X, pady=0, sticky="w")
        self.slider_salt_len.set(MAX_SALT_LEN)
        label_salt_len = customtkinter.CTkLabel(
            master=hash_password_frame,
            text=f"Salt length: {MAX_SALT_LEN}",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_salt_len.grid(row=11, column=0, sticky="w", padx=(DEFAULT_PADDING_X, 5), pady=0)
        label_salt_len_info = customtkinter.CTkLabel(
            master=hash_password_frame,
            text="[DEFAULT]",
            compound="left",
            font=("Roboto", 12, "bold"),
            anchor="w"
        )
        label_salt_len_info.grid(row=11, column=0, sticky="w", padx=(110, 5), pady=0)


    def get_root(self):
        return self.root


    def get_values(self):
        return self.values


    def get_value(self, widget_name):
        return self.values[widget_name]


    def set_value(self, widget_name, widget_value):
        self.values[widget_name] = widget_value


    def submit(self):
        #   -- User inputs
        self.set_value("username", self.input_field_username.get())
        self.set_value("master_password", self.input_field_password.get())
        self.set_value("master_password_again", self.input_field_password_confirmation.get())

        #   -- Hashing parameters
        self.set_value("time_cost", self.slider_time_cost.get())
        self.set_value("memory_cost", self.slider_memory_cost.get())
        self.set_value("parallelism", self.slider_parallelism.get())
        self.set_value("hash_len", self.slider_hash_len.get())
        self.set_value("salt_len", self.slider_salt_len.get())

        #   print(f"Values updated: {self.values}")
        self.controller.create_login()


    def show_error(self, widget, error_msg):
        if widget == "username_input":
            self.label_username_error.configure(text=error_msg)
            self.input_field_username.configure(border_color="red")
        elif widget == "master_password_input":
            self.label_password_error.configure(text=error_msg)
            self.input_field_password.configure(border_color="red")
        else:
            self.label_password_error.configure(text=error_msg)
            self.input_field_password_confirmation.configure(border_color="red")

        #   Bind events to clear the error when the user types
        self.input_field_username.bind("<KeyRelease>", lambda event: self.clear_error("username_input"))
        self.input_field_password.bind("<KeyRelease>", lambda event: self.clear_error("master_password_input"))
        self.input_field_password_confirmation.bind("<KeyRelease>", lambda event: self.clear_error("master_password_again_input"))


    def clear_error(self, widget):
        if widget == "username_input" and self.input_field_username.cget("border_color") == "red":
            self.label_username_error.configure(text="")
            self.input_field_username.configure(border_color="gray35")
        elif widget == "master_password_input" and self.input_field_password.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_password.configure(border_color="gray35")
        elif widget == "master_password_again_input" and self.input_field_password_confirmation.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_password_confirmation.configure(border_color="gray35")


    def on_close(self):
        #   Handle window close event.
        self.controller.del_window("sign_in_window")
        self.root.destroy()  # Destroys the window and resources


#   ------------ Slider method ----------------------------
    def update_slider_label(self, value, label_name, label_numbers, max_widget_value, label_info):
        label_numbers.configure(text=f"{label_name} {int(float(value))}")
        if value < (max_widget_value / 3):
            label_info.configure(text="[WEAK]", text_color="red")
        elif value < (max_widget_value / 2):
            label_info.configure(text="[MEDIUM]", text_color="dark orange")
        else:
            label_info.configure(text="[STRONG]", text_color="green")


#   ------------ Theme method ------------------------------
    def update_theme(self, colors):
        # Hide the window temporarily (prettier)
        self.view_utils.hide_window(self)

        BUTTON_TEXT_COLOR = colors["button_text_color"]
        TITLE_FG_COLOR = colors["title_fg_color"]
        self.title_frame.configure(fg_color=TITLE_FG_COLOR)
        self.button_cancel.configure(text_color=BUTTON_TEXT_COLOR)
        self.button_submit.configure(text_color=BUTTON_TEXT_COLOR)