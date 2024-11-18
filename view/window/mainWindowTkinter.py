import os
import customtkinter
import tkinter
from PIL import Image, ImageTk  # Si l'image n'est pas en format GIF ou PNG

base_dir = os.path.dirname(__file__)
customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('green')

MIN_WINDOW_WIDTH = 300
MIN_WINDOW_HEGIHT = 400

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 500
DEFAULT_WIDGET_HEIGHT = 35

TITLE_FONT_SIZE = 24

PARAGRAPH_FONT_SIZE = 14
MAIN_PARAGRAPH_PADDING_TOP_Y = 5
MAIN_PARAGRAPH_PADDING_BOTTOM_Y = 20

INPUT_TEXT_PADDING_BOTTOM = 10
INPUT_TEXT_PADDING_TOP= 10

BUTTON_FONT_SIZE = 18
BUTTON_PADDING_Y=25

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(__file__)
        self.root = customtkinter.CTkToplevel()
        self.root.title("Password Manager [PROTOTYPE]")

        # Set up window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        #   Window size
        self.root.geometry(f"{550}x{500}")
        #   Set minimum size for the window
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEGIHT)
        #   Values stored
        self.values = {}
        self.create_window()


    def get_root(self):
        return self.root


    def create_window(self):
        #   Using a tkinter Frame for a background without rounded corners
        title_frame = customtkinter.CTkFrame(master=self.get_root(), fg_color="#43d583", border_width=None, corner_radius=0)
        title_frame.pack(fill="both", expand=False)  # Takes full width with vertical padding
        #   Title label placed in tkinter frame
        title_label = customtkinter.CTkLabel(
            master=title_frame,
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
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            master=input_label_frame, 
            values=["Light", "Dark"], 
            command=self.change_appearance_mode_event,
            font=("Roboto", BUTTON_FONT_SIZE)
            )
        appearance_mode_optionemenu.grid(row=0, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, 0))
        
        #   Define the image path
        path_icon_app = os.path.join(self.base_dir, "../../assets/icon_app_v2.png")
        #   Row 1: Text paragraph
        #   Load the image with Pillow
        try:
            pil_image = Image.open(path_icon_app).resize((200, 200), Image.LANCZOS)  # Resize
            image_icon_app = ImageTk.PhotoImage(pil_image)
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
        #   Paragraph
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
        
        #   Row 3: Username input
        input_field_1 = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Username", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT
            )
        input_field_1.grid(row=3, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y)
        #   Row 4: Master password input
        input_field_2 = customtkinter.CTkEntry(
            master=input_label_frame, 
            placeholder_text="Master password", 
            width=DEFAULT_WIDGET_WIDTH, 
            height=DEFAULT_WIDGET_HEIGHT
            )
        input_field_2.grid(row=4, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=(DEFAULT_PADDING_Y, 0))

        #   Row 5: Label with text and image
        path_icon_info = os.path.join(self.base_dir, "../../assets/icon_info.png")
        try:
            pil_image = Image.open(path_icon_info).resize((30, 30), Image.LANCZOS)  # Resize
            image_icon_info = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            image_icon_info = None
        #   Add label with image
        label_with_image = customtkinter.CTkLabel(
            master=input_label_frame,
            text="  The master password should be remembered by the user!",
            image=image_icon_info,
            compound="left",
            font=("Roboto", 12),
            anchor="w"  # Align to the left
        )
        label_with_image.grid(row=5, column=0, sticky="w", padx=DEFAULT_PADDING_X, pady=(0, 20))
        
        #   Define a grid(Frame)
        input_label_frame.grid_columnconfigure(0, weight=1)

        #   Row 6: Buttons / Submit buttons
        #   Frame for buttons
        button_login = customtkinter.CTkButton(
            master=input_label_frame,
            text="Sign in", 
            command=self.sign_in,
            width=(input_field_1.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE)
        )
        button_login.grid(row=6, column=0, sticky="w", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))

        button_sign_in = customtkinter.CTkButton(
            master=input_label_frame, 
            text="Login", 
            command=self.login,
            width=(input_field_1.winfo_reqwidth()/3),
            font=("Roboto", BUTTON_FONT_SIZE),
        )
        button_sign_in.grid(row=6, column=0, sticky="e", padx=(5, 5), pady=(0, DEFAULT_PADDING_Y))


    def login(self):
        print('test')    


    def sign_in(self):
        print('sign in')
    

    def on_close(self):
        #   Handle window close event.
        self.root.quit()  # Stops the mainloop
        self.root.destroy()  # Destroys the window and resources


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def update_wraplength(self, paragraph_label):
        #   Adjusts the text width to the new window width
        max_width = 380  # Maximum width to prevent text from becoming invisible
        current_width = self.root.winfo_width() - 80
        paragraph_label.configure(wraplength=min(current_width, max_width))


    #   Retrieve text from the input fields and send it.
    def send_data(self):
        username = self.input_field_1.get()
        master_password = self.input_field_2.get()

        # Log the data or send it to a function for further processing
        print(f"Username: {username}")
        print(f"Master Password: {master_password}")

        # Example: Sending data to another function 
        self.process_login(username, master_password)


    #   Process the retrieved data (example: validate or store).
    def process_login(self, username, master_password):
        if username and master_password:
            print("Processing login...")
            #TODO : If username + master_password == None then send [ERROR] output to user using red colors
        else:
            print("Please fill in all fields.")


if __name__ == "__main__":
    window = MainWindow()
    window.get_root().mainloop()