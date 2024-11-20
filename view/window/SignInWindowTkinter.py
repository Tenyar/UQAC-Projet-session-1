import os
import customtkinter
from utility.ViewFunctionsUtility import hide_window

MIN_WINDOW_WIDTH = 495
MIN_WINDOW_HEGIHT = 375

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 500
DEFAULT_WIDGET_HEIGHT = 35

TITLE_FONT_SIZE = 24

PARAGRAPH_FONT_SIZE = 16
MAIN_PARAGRAPH_PADDING_TOP_Y = 10
MAIN_PARAGRAPH_PADDING_BOTTOM_Y = 20

INPUT_TEXT_PADDING_BOTTOM = 10
INPUT_TEXT_PADDING_TOP= 10

BUTTON_FONT_SIZE = 18
BUTTON_PADDING_Y=25

class SignInWindowTkinter(customtkinter.CTk):
    def __init__(self, controller):
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.controller = controller
        self.root = customtkinter.CTkToplevel()
        self.root.title("Sign in [PROTOTYPE]")

        #   Ensure the window is on top and grabs focus
        self.root.attributes("-topmost", True)
        self.root.focus_force()

        #   Set up window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        #   Window size
        self.root.geometry(f"{550}x{375}")
        #   Set minimum size for the window
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEGIHT)
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

        #   Main frame with margins to center the content
        main_frame = customtkinter.CTkFrame(master=self.get_root())
        main_frame.pack(fill="both", expand=True)

        #   Create a frame for input fields and labels
        input_label_frame = customtkinter.CTkFrame(master=main_frame)
        input_label_frame.pack(pady=DEFAULT_PADDING_Y, padx=DEFAULT_PADDING_X, expand=True)

        #   Row 0: Text paragraph
        #   Paragraph
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
        #   Row 1: Username input
        self.input_field_1 = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Username", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT
            )
        self.input_field_1.grid(row=2, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)

                
        #   Row 2: Master password error label
        self.label_password_error = customtkinter.CTkLabel(
            master=input_label_frame,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"  # Align to the left
        )
        self.label_password_error.grid(row=3, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 2: Master password input
        self.input_field_2 = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_field_2.grid(row=4, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 3: Label with text
        #   Add label
        label_info = customtkinter.CTkLabel(
            master=input_label_frame,
            text="  The master password should be remembered by the user!",
            compound="left",
            font=("Roboto", 12),
            anchor="w"  # Align to the left
        )
        label_info.grid(row=5, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(0, DEFAULT_PADDING_Y))

        #   Row 3: Ask master password input again for confirmation
        self.input_field_3 = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password again", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_field_3.grid(row=6, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=(0, 20))        

        #   Define a grid(Frame)
        input_label_frame.grid_columnconfigure(0, weight=1)

        #   Row 4: Buttons / Submit buttons
        #   Frame for buttons
        self.button_cancel = customtkinter.CTkButton(
            master=input_label_frame,
            text="Cancel", 
            command=self.on_close,
            width=(self.input_field_1.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_cancel.grid(row=7, column=0, sticky="w", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))
        self.button_submit = customtkinter.CTkButton(
            master=input_label_frame, 
            text="Submit", 
            command=self.submit,
            width=(self.input_field_1.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_submit.grid(row=7, column=0, sticky="e", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))


    def get_root(self):
        return self.root


    def get_values(self):
        return self.values


    def get_value(self, widget_name):
        return self.values[widget_name]


    def set_value(self, widget_name, widget_value):
        self.values[widget_name] = widget_value


    def submit(self):
        self.set_value("username", self.input_field_1.get())
        self.set_value("master_password", self.input_field_2.get())
        self.set_value("master_password_again", self.input_field_3.get())

        print(f"Values updated: {self.values}")
        self.controller.create_login()


    def show_error(self, widget, error_msg):
        if widget == "username_input":
            self.label_username_error.configure(text=error_msg)
            self.input_field_1.configure(border_color="red")
        elif widget == "master_password_input":
            self.label_password_error.configure(text=error_msg)
            self.input_field_2.configure(border_color="red")
        else:
            self.label_password_error.configure(text=error_msg)
            self.input_field_3.configure(border_color="red")

        #   Bind events to clear the error when the user types
        self.input_field_1.bind("<KeyRelease>", lambda event: self.clear_error("username_input"))
        self.input_field_2.bind("<KeyRelease>", lambda event: self.clear_error("master_password_input"))
        self.input_field_3.bind("<KeyRelease>", lambda event: self.clear_error("master_password_again_input"))


    def clear_error(self, widget):
        if widget == "username_input" and self.input_field_1.cget("border_color") == "red":
            self.label_username_error.configure(text="")
            self.input_field_1.configure(border_color="gray35")
        elif widget == "master_password_input" and self.input_field_2.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_2.configure(border_color="gray35")
        elif widget == "master_password_again_input" and self.input_field_3.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_3.configure(border_color="gray35")


    def on_close(self):
        #   Handle window close event.
        self.controller.del_window("sign_in_window")
        self.root.destroy()  # Destroys the window and resources


#   ------------ Theme method ------------------------------
    def update_theme(self, colors):
        hide_window(self)

        BUTTON_TEXT_COLOR = colors["button_text_color"]
        TITLE_FG_COLOR = colors["title_fg_color"]
        self.title_frame.configure(fg_color=TITLE_FG_COLOR)
        self.button_cancel.configure(text_color=BUTTON_TEXT_COLOR)
        self.button_submit.configure(text_color=BUTTON_TEXT_COLOR)