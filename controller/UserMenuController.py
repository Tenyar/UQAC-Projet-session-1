import shutil
import os
import view.window.UserMenuWindowTkinter as user_menu_window
from utility.functionUtility import is_field_not_empty
from model.HashModel import HashModel
from utility.ViewFunctionsUtility import ViewFunctionsUtility


class UserMenuController:
    def __init__(self, mainController, EncryptionManager, username, dao):
        self.username = username
        self.encryption_manager = EncryptionManager
        self.mainController = mainController
        self.running = True
        self.daoConnect = dao
        self.view_utils = ViewFunctionsUtility(self)

        self.open_windows = {}


    def get_running(self):
        return self.running


    def set_running(self, state: bool):
        self.running = state


    def get_username(self):
        return self.username


    def get_window(self, window_name):
        try:
            return self.open_windows[window_name]
        except KeyError:
            return


    def set_window(self, window_name, value):
        self.open_windows[window_name] = value


    def run(self):
        while self.get_running():
            #   Call the utility function to display the menu
            self.set_window("user_menu_window", user_menu_window.UserMenuWindowTkinter(self))
            self.get_window("user_menu_window").get_root().mainloop()


    def delete_account(self):
        self.daoConnect.close()
        self.ViewFunctionsUtility.open_ask_password_window()
        # Wait for the password window to close
        if self.ViewFunctionsUtility.getget_window("ask_password_window") is not None:
            self.ViewFunctionsUtility.getget_window("ask_password_window").wait_window()

        # Process the password or cancellation
        if self.password_input is None:
            print("Action canceled by the user.")
        else:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  #    Climb up one level to reach the root
            folder_path = os.path.join(project_root, 'model', 'database', self.username)
            if os.path.exists(folder_path):
                try:
                    # Use shutil.rmtree to delete the folder and all contents
                    shutil.rmtree(folder_path)
                    print("Account folder and contents successfully deleted.")
                except Exception as e:
                    print(f"Error while deleting folder: {e}")
            else:
                print("Folder not found, nothing to delete.")
            self.disconnect()
            # Add logic to validate and delete the account here



        # Print the folder path for verification
        #print(f"Folder path to delete: {folder_path}")
        
        #print("Folder exists:", os.path.exists(folder_path))


    def disconnect(self, window, password):
        #   Wait for the password window to close
        window.destroy()
        if is_field_not_empty(password):
            #   master password & verify it's authenticity and is veracity
            self.daoConnect.connect_db()
            master_password_db = self.daoConnect.get_fullhashed_master_password(self.username)
            data_hash_db = self.daoConnect.get_hashing_data(self.username)
            if HashModel.verify_password(data_hash_db, password, master_password_db):
                self.mainController.get_encryption_manager().encrypt_on_exit(password)
                self.get_window("user_menu_window").quit()
                self.get_window("user_menu_window").destroy()
                self.running = False
                self.mainController.set_running(True)
                self.mainController.run()
                return
            else:
                self.view_utils.os_error_message('Password error', "Wrong password")
                return