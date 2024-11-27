import os
import customtkinter
from PIL import Image
from customtkinter import CTkImage
from utility.ViewFunctionsUtility import ViewFunctionsUtility

MIN_WINDOW_WIDTH = 520
MIN_WINDOW_HEIGHT = 500

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 500
DEFAULT_WIDGET_HEIGHT = 35

TITLE_FONT_SIZE = 24
TITLE_FG_COLOR = "#43d583"

PARAGRAPH_FONT_SIZE = 15
MAIN_PARAGRAPH_PADDING_TOP_Y = 5
MAIN_PARAGRAPH_PADDING_BOTTOM_Y = 20

INPUT_TEXT_PADDING_BOTTOM = 10
INPUT_TEXT_PADDING_TOP= 10

BUTTON_FONT_SIZE = 18
BUTTON_PADDING_Y = 25
BUTTON_TEXT_COLOR = "Black"


class MainWindowTkinter(customtkinter.CTk):
    def __init__(self, controller):
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.controller = controller
        self.view_utils = ViewFunctionsUtility(self)

        #   Default system theme
        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('green')

        self.root = customtkinter.CTkToplevel()
        self.root.title("Password Manager [PROTOTYPE]")
        #   Set up window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        #   Window size
        self.root.geometry(f"{550}x{500}")
        #   Set minimum size for the window
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        #   Values stored
        self.values = {}

        # Create UI components
        self.create_window()


    def create_window(self):
        #   Using a tkinter Frame for a background without rounded corners
        self.title_frame = customtkinter.CTkFrame(master=self.get_root(), fg_color="#43d583", border_width=None, corner_radius=0)
        self.title_frame.pack(fill="both", expand=False)  # Takes full width with vertical padding
      
        #   Title label placed in tkinter frame
        title_label = customtkinter.CTkLabel(
            master=self.title_frame,
            text="Connection",
            font=("Roboto", TITLE_FONT_SIZE)
        )
        title_label.pack(pady=10)  # Spacing around text

        #   Main frame with margins to center the content
        main_frame = customtkinter.CTkFrame(master=self.get_root())
        main_frame.pack(fill="both", expand=True)

        #   Create a frame for input fields and labels
        input_label_frame = customtkinter.CTkFrame(master=main_frame)
        input_label_frame.pack(pady=DEFAULT_PADDING_Y, padx=DEFAULT_PADDING_X, expand=True)
        
        #   Row 0: Theme option selector
        #   Frame for changing the application themes
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            master=input_label_frame, 
            values=["Light", "Dark"], 
            command=self.change_appearance_mode,
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
            )
        self.appearance_mode_optionemenu.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, 0))
        
        #   Define the image path
        path_icon_app = os.path.join(self.base_dir, "../../assets/icon_app_v2.png")
        #   Row 1: Text paragraph
        try:
            pil_image = Image.open(path_icon_app)   # Open the image with Pillow
            image_icon_app = CTkImage(pil_image, size=(130, 130))   # Convert to CTkImage
        except Exception as e:
            print(f"Error loading image: {e}")
            image_icon_app = None
        #   Add label with image
        label_with_image = customtkinter.CTkLabel(
            master=input_label_frame,
            image=image_icon_app,  # Use loaded image
            text=""
        )
        label_with_image.grid(row=1, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)
        
        #   Row 2: Text paragraph
        paragraph_text = (
            "Welcome to the password manager!\n"
            "Here, you will register, manage and secure all of your password in one area.\n"
            "Please enter your username and master password to access your account."
        )
        #  Automatically adjust text width
        paragraph_label = customtkinter.CTkLabel(
            master=input_label_frame,
            text=paragraph_text,
            font=("Roboto", PARAGRAPH_FONT_SIZE),
            wraplength=DEFAULT_WIDGET_WIDTH  # Limits the width of the text so that it displays on multiple lines
        )
        paragraph_label.grid(row=2, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=(MAIN_PARAGRAPH_PADDING_TOP_Y, DEFAULT_PADDING_Y))
        
        #   Row 3-4: Username input
        self.label_username_error = customtkinter.CTkLabel(
            master=input_label_frame,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"  # Align to the left
        )
        self.label_username_error.grid(row=3, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        self.input_field_username = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Username", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT
            )
        self.input_field_username.grid(row=4, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)
        #   Row 5-6: Master password input
        self.label_password_error = customtkinter.CTkLabel(
            master=input_label_frame,
            text="",
            compound="left",
            font=("Roboto", 12, "bold"),
            text_color="red",
            anchor="w"  # Align to the left
        )
        self.label_password_error.grid(row=5, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=0)
        self.input_field_password = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT,
            show="*"
            )
        self.input_field_password.grid(row=6, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)

        #   Row7: Label with text and image
        path_icon_info = os.path.join(self.base_dir, "../../assets/icon_info.png")
        try:
            pil_image = Image.open(path_icon_info)
            image_icon_info = CTkImage(pil_image, size=(25, 25))
        except Exception as e:
            print(f"Error loading image: {e}")
            image_icon_info = None
        label_with_image = customtkinter.CTkLabel(
            master=input_label_frame,
            text="  The master password should be remembered by the user!",
            image=image_icon_info,
            compound="left",
            font=("Roboto", 12),
            anchor="w"  # Align to the left
        )
        label_with_image.grid(row=7, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(5,5))
        
        input_label_frame.grid_columnconfigure(0, weight=1)

        #   Row 8: Buttons / Submit buttons
        self.button_sign_in = customtkinter.CTkButton(
            master=input_label_frame,
            text="Sign in", 
            command=self.sign_in,
            width=(self.input_field_username.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_sign_in.grid(row=8, column=0, sticky="w", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))

        self.button_login = customtkinter.CTkButton(
            master=input_label_frame, 
            text="Login", 
            command=self.login,
            width=(self.input_field_username.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
            text_color="black"
        )
        self.button_login.grid(row=8, column=0, sticky="e", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))
            #   Bind events to clear the error when the user types
        self.input_field_username.bind("<KeyRelease>", lambda event: self.clear_error("username_input"))
        self.input_field_password.bind("<KeyRelease>", lambda event: self.clear_error("master_password_input"))


    def get_root(self):
        return self.root


    def get_value(self, widget):
        return self.values[widget]


    def get_controller(self):
        return self.controller


    def get_appearance_mode_optionemenu(self):
        return self.appearance_mode_optionemenu


    def login(self):
        #   Retrieve text from the input fields and send it.
        self.values["username"] = self.input_field_username.get()
        self.values["master_password"] = self.input_field_password.get()
        self.get_controller().connect_login()


    def sign_in(self):
        self.get_controller().start_sign_in()
    

    def clear_error(self, widget):
        if widget == "username_input" and self.input_field_username.cget("border_color") == "red":
            self.label_username_error.configure(text="")
            self.input_field_username.configure(border_color="gray35")
        elif widget == "master_password_input" and self.input_field_password.cget("border_color") == "red":
            self.label_password_error.configure(text="")
            self.input_field_password.configure(border_color="gray35")


    def on_close(self):
        print("[DEBUG] on_close called [MainWindow]")
        #   Handle window close event.
        self.root.quit()  # Stops the mainloop
        self.root.destroy()  # Destroys the window and resources
        self.get_controller().set_running(False)
        self.get_controller().exit_app()


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
        self.view_utils.hide_window(self)

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