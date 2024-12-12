#   Add the project root directory to sys.path (for importing custom classes)
import sys
import os
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import view.window.MainWindowTkinter as main_window
import view.window.SignInWindowTkinter as sign_in_window

#   Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from utility.functionUtility import is_field_not_empty
from utility.ViewFunctionsUtility import ViewFunctionsUtility
from UserMenuController import UserMenuController
from model.DAO import DAO
from model.HashModel import HashModel
from model.UserModel import UserModel # Argond2(id) is used in this prototype for better security (longer time for hash)
from model.EncryptionModel import EncryptionModel
from model.EncryptionManager import EncryptionManager
#####################################################################################
#          #######      #               ##########      
#        #              #                   #
#       #               #                   #
#       #               #                   #           (command line interface)
#        #              #                   #
#          #######      ########        ##########
#####################################################################################
class MainController:
    def __init__(self):
        self.running = True
        self.daoConnect = None
        self.user_master_password = None
        self.view_utils = ViewFunctionsUtility(self)
        self.user_menu_controller = None
        self.open_windows = {}
        self.current_window_theme = "Light" #   Theme by default

        # Initialize the encryption manager and register the exit encryption
        self.encryption_manager = EncryptionManager()


    def get_encryption_manager(self):
        return self.encryption_manager


    def get_user_master_password(self):
        return self.user_master_password


    def get_current_window_theme(self):
        return self.current_window_theme

    
    def set_current_window_theme(self, theme):
        self.current_window_theme = theme


    def get_window(self, window_name):
        try:
            return self.open_windows[window_name]
        except KeyError:
            return


    def set_window(self, window_name, value):
        self.open_windows[window_name] = value


    def del_window(self, window_name):
        del self.open_windows[window_name]


    def get_windows(self):
        return self.open_windows


    def get_user_menu_controller(self):
        return self.user_menu_controller


    def get_running(self):
        return self.running


    def set_running(self, state: bool):
        self.running = state


    def get_dao(self):
        return self.daoConnect


    def set_dao(self, daoConnect: object):
        if(isinstance(daoConnect, DAO)):
            self.daoConnect = daoConnect
        else:
            self.daoConnect = None


    def set_user_master_password(self, user_master_password: str):
            self.user_master_password = user_master_password


    def exit_app(self):
        sys.exit(0)


    def run(self):
        while self.get_running():
            self.set_window("main_window", main_window.MainWindowTkinter(self))
            self.get_window("main_window").get_root().mainloop()


    def start_sign_in(self):
        # Create and open the sign-in window
        if not self.get_window("sign_in_window"):
            self.set_window("sign_in_window", sign_in_window.SignInWindowTkinter(self))
            self.theme_change_all(self.get_current_window_theme())


    def create_login(self):
        #   Variables
        username = self.get_window("sign_in_window").get_value("username")
        master_password = self.get_window("sign_in_window").get_value("master_password")
        master_password_again = self.get_window("sign_in_window").get_value("master_password_again")

        hash_params = {
            "time_cost": self.get_window("sign_in_window").get_value("time_cost"),
            "memory_cost": self.get_window("sign_in_window").get_value("memory_cost"),
            "parallelism": self.get_window("sign_in_window").get_value("parallelism"),
            "hash_len": self.get_window("sign_in_window").get_value("hash_len"),
            "salt_len": self.get_window("sign_in_window").get_value("salt_len")
        }

        fields = [
            {"key": "username", "error_key": "username_input", "error_message": "You need to enter a username!"},
            {"key": "master_password", "error_key": "master_password_input", "error_message": "You need to enter a password!"},
            {"key": "master_password_again", "error_key": "master_password_again_input", "error_message": "You need to enter the password again!"}
        ]
        #   Check for errors, If fields are empty
        for field in fields:
            value = self.get_window("sign_in_window").get_value(field["key"])
            if not is_field_not_empty(value):
                self.get_window("sign_in_window").show_error(field["error_key"], field["error_message"])
                return

        if master_password != master_password_again:
            self.get_window("sign_in_window").show_error("master_password_input", "Passwords doesn't match!")
            return
        else:
            self.set_dao(DAO(username))
            #   Error management of the unique contraint of a user
            if self.get_dao().get_folder_by_username():
                self.view_utils.os_error_message("Data base ERROR", f"the username \"{username}\" is arleady taken, please retry ")
                return

        #   Verify if the user already exist
        if self.get_dao().get_folder_by_username():
            self.view_utils.os_error_message('Database error', "User already exist, please retry")
            return
        
        #   Close the sign in window
        self.get_window("sign_in_window").on_close()
        
        #   Correct the paths for each file that must be created with the new username
        self.get_dao().set_absolute_paths()
        self.get_dao().create_db()

        #   Add the master password for the encryption + path of the files to be encrypted
        self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
        self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)

        #   Create a user object
        user = UserModel(username, master_password, hash_params)

        #   Establishing connection to the DB is done in this method to be regroup frequent use of the 'connect' method
        self.get_dao().create_user(user)
        self.get_dao().close()

        #   Encrypt databases files with master password
        EncryptionModel.encrypt_db(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME, master_password, self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
        EncryptionModel.encrypt_db(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME, master_password, self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)


    def connect_login(self):
        username = self.get_window("main_window").get_value("username")
        master_password = self.get_window("main_window").get_value("master_password")

        if not is_field_not_empty(username):
            self.get_window("main_window").show_error("username_input", "You need to enter a username!")
            return
        elif not is_field_not_empty(master_password):
            self.get_window("main_window").show_error("master_password_input", "You need to enter a password!")
            return
        
        self.set_dao(DAO(username))

        try:
            #   Decrypt the database to a temporary file when needed
            EncryptionModel.decrypt_db(self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_USER_NAME, master_password, self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
            EncryptionModel.decrypt_db(self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME, master_password, self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)
        except Exception as e:
            self.view_utils.os_error_message('Database encryption error', 'Failed to dencrypt database files (Wrong username)')
            return

        if self.get_dao().connect_db() == False:
            self.get_dao().close()
            self.view_utils.os_error_message('Database error', "User don't exist, please retry")
            return

        #   master password & verify it's authenticity and is veracity
        master_password_db = self.get_dao().get_fullhashed_master_password(username)
        data_hash_db = self.get_dao().get_hashing_data(username)
        try:
            if HashModel.verify_password(data_hash_db, master_password, master_password_db):
                #   Close main window
                self.set_running(False)
                self.get_window("main_window").get_root().quit()
                self.get_window("main_window").get_root().destroy()
                if self.get_window("sign_in_window"):
                    self.get_window("sign_in_window").get_root().destroy()
                #   Set the password to encrypt databases
                self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
                self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)
                #   Launch the user menu controller
                self.set_user_master_password(master_password)
                self.get_dao().close()
                self.get_windows().clear()
                self.user_menu_controller = UserMenuController(self, self.encryption_manager, username, self.get_dao())
                self.get_user_menu_controller().run()
            else:
                self.view_utils.os_error_message('Password error', "User denied!")
        except Exception as e: 
            print("\n[Exception]!", str(e))


    def theme_change_all(self, new_theme):
        self.set_current_window_theme(new_theme)
        colors = self.view_utils.get_theme_colors_main(new_theme)
        try:
            windows = self.get_windows()
            windows["user_menu_window"] = self.get_user_menu_controller().get_window("user_menu_window")
        except Exception as e:
            pass
        for view_name in windows:
            self.get_window(view_name).update_theme(colors)

if __name__ == "__main__":
    controller = MainController()  # Create an instance of MainController
    controller.run()  # Call the main menu method to start the program