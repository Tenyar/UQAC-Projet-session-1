#   Utility class with methods to manage views(windows) behavior
#   Error messages
from tkinter import messagebox
import customtkinter

DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10
DEFAULT_WIDGET_WIDTH = 350
DEFAULT_WIDGET_HEIGHT = 35


class ViewFunctionsUtility:
    def __init__(self, controller):
        self.controller = controller
        self.open_windows = {}


    def get_controller(self):
        return self.controller


    def get_window(self, window_name):
        return self.open_windows.get(window_name)


    def get_password_field_value(self):
        return self.input_ask_password.get()


    #   Return an dictionnary of widget : style_settings
    def get_theme_colors_main(self, theme):
        if theme.lower() == "light":
            return {"button_text_color": "black", "title_fg_color": "#43d583"}
        else:
            return {"button_text_color": "white", "title_fg_color": "#34a766"}


    def hide_window(self, window):
        window.get_root().withdraw()
        # Wait for 250 milliseconds, then reopen and enable interaction
        window.get_root().after(250, self.reopen_with_theme, window)


    def reopen_with_theme(self, window):
        # Reopen the window
        window.get_root().deiconify() 
        # Re-enable interaction in the option menu
        if hasattr(window, 'appearance_mode_optionemenu'):
            window.appearance_mode_optionemenu.configure(state="normal")


    def open_confirmation_window(self):
        if not self.open_windows["confirmation_window"]:
            root = customtkinter.CTkToplevel()
            root.title(f"Confirmation window [PROTOTYPE]")
            root.geometry(f"{400}x{150}")
            root.grid_rowconfigure(0, weight=1)  
            root.grid_columnconfigure(0, weight=1)

            main_frame = customtkinter.CTkFrame(master=root)
            main_frame.pack(fill="both", expand=True,)
            main_frame.grid_rowconfigure(0, weight=1) 
            main_frame.grid_columnconfigure(0, weight=1) 
            #   Create a frame for input fields and labels
            sub_frame = customtkinter.CTkFrame(master=main_frame)
            sub_frame.grid(row=0, column=0, padx=0, sticky="")


            title_label = sub_frame.CTkLabel(
                    master=main_frame,
                    text="Connection",
                    font=("Roboto", 16, "bold")
                )
            title_label.grid(row=0, column=0, sticky="", padx=(5, 5), pady=(0, 0))
            button_refuse = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Refuse", 
                    width=100,
                    fg_color="#c25364",
                    hover_color="#9f4250",
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.confirm_choice(False),
                    cursor="hand2"
                )
            button_refuse.grid(row=1, column=0, sticky="w", padx=(5, 5), pady=(0, 0))
            button_accept = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Accept", 
                    width=100,
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.confirm_choice(True),
                    cursor="hand2"
                )
            button_accept.grid(row=1, column=0, sticky="e", padx=(5, 5), pady=(0, 0))


    def confirme_choice(self, accepted):
        if accepted:
            self.password_input = self.input_field_password.get()
        else:
            self.password_input = None
        self.open_windows["ask_password_window"] = None
        self.destroy()
        

    def open_ask_password_window(self, window_root):
        if not self.get_window("ask_password_window") and not self.get_window("confirmation_window"):
            self.open_windows["ask_password_window"] = self
            root = customtkinter.CTkToplevel()
            root.title(f"Password confirmation window [PROTOTYPE]")
            root.geometry(f"{400}x{150}")
            root.grid_rowconfigure(0, weight=1) 
            root.grid_columnconfigure(0, weight=1)
            root.attributes("-topmost", True)
            #//root.focus_force()

            main_frame = customtkinter.CTkFrame(master=root)
            main_frame.pack(fill="both", expand=True,)
            main_frame.grid_rowconfigure(0, weight=1) 
            main_frame.grid_columnconfigure(0, weight=1) 
            #   Create a frame for input fields and labels
            sub_frame = customtkinter.CTkFrame(master=main_frame)
            sub_frame.grid(row=0, column=0, padx=0, sticky="")

            #// Temporary variable to store the password
            #//self.password_var = customtkinter.StringVar()
            
            title_label = customtkinter.CTkLabel(
                    master=sub_frame,
                    text="Enter master password",
                    font=("Roboto", 16, "bold")
                )
            title_label.grid(row=0, column=0, sticky="", padx=DEFAULT_PADDING_X, pady=0)

            self.input_ask_password = customtkinter.CTkEntry(
                master=sub_frame, 
                placeholder_text="Master password", 
                width=DEFAULT_WIDGET_WIDTH, 
                height=DEFAULT_WIDGET_HEIGHT,
                show="*"
            )
            self.input_ask_password.grid(row=1, column=0, sticky="we", padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y)

            button_cancel = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Cancel", 
                    width=100,
                    fg_color="#c25364",
                    hover_color="#9f4250",
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.ask_password(None, False, root, window_root),
                    cursor="hand2"
                )
            button_cancel.grid(row=2, column=0, sticky="w", padx=(5, 5), pady=(0, 0))
            button_accept = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Accept", 
                    width=100,
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.ask_password(self.input_ask_password.get(), True, root, window_root),
                    cursor="hand2"
                )
            button_accept.grid(row=2, column=0, sticky="e", padx=(5, 5), pady=(0, 0))

            #   Bind the on-close event
            root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_ask_password_window(root))


    def ask_password(self, password, accepted, root, window_root):
        if "ask_password_window" in self.open_windows:
            if not accepted:
                return
            else:
                del self.open_windows["ask_password_window"]
                self.controller.disconnect(root, password)
                window_root.destroy()
                #//   self.controller.get_encryption_manager().encrypt_on_exit(password)
        else:
            print("Error: 'ask_password_window' key does not exist in open_windows.")


    def on_close_ask_password_window(self, root):
        del self.open_windows["ask_password_window"]
        root.quit()
        root.destroy()


    def os_error_message(self, error, message):
        messagebox.showerror(error, f'[ERROR] {message}')