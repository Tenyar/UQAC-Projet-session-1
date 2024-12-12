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


    def get_root(self):
        return self.root


    def get_theme_colors_main(self, theme):
    #   Return an dictionnary of widget : style_settings
        print('THEME LOWER : ', theme.lower())
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


    def open_delete_service_confirmation_window(self, args):
        if not self.get_window("confirmation_window"):
            self.open_windows["confirmation_window"] = self
            self.root = customtkinter.CTkToplevel()
            self.root.title(f"Confirmation window [PROTOTYPE]")
            self.root.geometry(f"{300}x{100}")
            self.root.grid_rowconfigure(0, weight=1) 
            self.root.grid_columnconfigure(0, weight=1)
            self.root.attributes("-topmost", True)

            main_frame = customtkinter.CTkFrame(master=self.root)
            main_frame.pack(fill="both", expand=True,)
            main_frame.grid_rowconfigure(0, weight=1) 
            main_frame.grid_columnconfigure(0, weight=1) 
            #   Create a frame for input fields and labels
            sub_frame = customtkinter.CTkFrame(master=main_frame)
            sub_frame.grid(row=0, column=0, padx=0, pady=0, sticky="")

            title_label = customtkinter.CTkLabel(
                master=sub_frame,
                width=300,
                text="Confirm your choice",
                font=("Roboto", 16, "bold")
            )
            title_label.grid(row=0, column=0, sticky="ew", pady=20)

            button_cancel = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Cancel", 
                    width=100,
                    fg_color="#c25364",
                    hover_color="#9f4250",
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.delete_service_confirme_choice(False, args),
                    cursor="hand2"
                )
            button_cancel.grid(row=1, column=0, sticky="w", padx=(5, 5), pady=(0, 0))
            button_accept = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Accept", 
                    width=100,
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.delete_service_confirme_choice(True, args),
                    cursor="hand2"
                )
            button_accept.grid(row=1, column=0, sticky="e", padx=(5, 5), pady=(0, 0))

            #   Bind the on-close event
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_confirmation_window())


    def delete_service_confirme_choice(self, accepted, args):
        self.open_windows["confirmation_window"] = None
        self.get_root().destroy()
        if accepted:
            self.get_controller().delete_chest_service(args[1].cget("text"), args[2].cget("text"))
            args[0].setup_chest_tab()
            return True
        else:
            return False
    

    def on_close_confirmation_window(self):
        del self.open_windows["confirmation_window"]
        self.root.destroy()
        

    def open_ask_password_window(self, tab_name):
        if not self.get_window("ask_password_window") and not self.get_window("confirmation_window"):
            self.open_windows["ask_password_window"] = self
            self.root = customtkinter.CTkToplevel()
            self.root.title(f"Password confirmation window [PROTOTYPE]")
            self.root.geometry(f"{400}x{150}")
            self.root.grid_rowconfigure(0, weight=1) 
            self.root.grid_columnconfigure(0, weight=1)
            self.root.attributes("-topmost", True)

            main_frame = customtkinter.CTkFrame(master=self.root)
            main_frame.pack(fill="both", expand=True,)
            main_frame.grid_rowconfigure(0, weight=1) 
            main_frame.grid_columnconfigure(0, weight=1)
            #   Create a frame for input fields and labels
            sub_frame = customtkinter.CTkFrame(master=main_frame)
            sub_frame.grid(row=0, column=0, padx=0, sticky="")

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
                    command=lambda: self.on_close_ask_password_window(),
                    cursor="hand2"
                )
            button_cancel.grid(row=2, column=0, sticky="w", padx=(5, 5), pady=(0, 0))
            button_accept = customtkinter.CTkButton(
                    master=sub_frame, 
                    text="Accept", 
                    width=100,
                    font=("Roboto", 16, "bold"),
                    text_color="black",
                    command=lambda: self.ask_password(self.input_ask_password.get(), True, tab_name),
                    cursor="hand2"
                )
            button_accept.grid(row=2, column=0, sticky="e", padx=(5, 5), pady=(0, 0))

            #   Bind the on-close event
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_ask_password_window())


    def ask_password(self, password, accepted, tab_name):
        if "ask_password_window" in self.open_windows:
            if not accepted:
                return
            else:
                del self.open_windows["ask_password_window"]
                self.get_root().destroy()
                if tab_name == "on_close":
                    self.get_controller().disconnect(password)
                elif tab_name == "suppress_account":
                    self.get_controller().delete_account(password)
        else:
            print("Error: 'ask_password_window' key does not exist in open_windows.")


    def on_close_ask_password_window(self):
        del self.open_windows["ask_password_window"]
        self.root.destroy()


    def os_error_message(self, error, message):
        messagebox.showerror(error, f'[ERROR] {message}')

    
    def os_info_message(self, title, message):
        messagebox.showinfo(title, f'[INFO] {message}')