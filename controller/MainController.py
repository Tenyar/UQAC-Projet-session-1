import sys
import os

# Add the project root directory to sys.path (for importing custom classes)
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import view.MainView as MainView
import atexit

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from UserMenuController import UserMenuController
from model.DAO import DAO
from model.HashModel import HashModel
from getpass import getpass # Utility to hide inputs when writing a password
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
        self.main_view = MainView
        self.daoConnect = None
        self.user_master_password = None
        # Initialize the encryption manager and register the exit encryption
        self.encryption_manager = EncryptionManager()
        atexit.register(self.encryption_manager.encrypt_on_exit)


    def get_encryption_manager(self):
        return self.encryption_manager


    def get_user_master_password(self):
        return self.user_master_password

    
    def get_dao(self):
        return self.daoConnect


    def set_running(self, state: bool):
            self.running = state


    def set_dao(self, daoConnect: object):
        if(isinstance(daoConnect, DAO)):
            self.daoConnect = daoConnect
        else:
            self.daoConnect = None
    

    def set_user_master_password(self, user_master_password: str):
            self.user_master_password = user_master_password


    def run(self):
        while self.running:
            #   Call the utility function to display the menu
            self.main_view.dispaly_main_menu()
            try:
                user_choice = int(input("\nEnter your choice: "))
            except Exception as e:
                print('[ERROR] wrong input given!')
                user_choice = None
            match user_choice:
                case 1:
                    self.create_login()  # Call the instance method
                case 2:
                    self.connect_login()
                case 3:
                    print("\nExiting the program...")
                    self.running = False
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def create_login(self):
        print("Creating a new login")
        user_name = input("\nEnter your name/email: ")  # User's name/email
        #   Connect/Create a database in the username folder
        self.set_dao(DAO(user_name))
        #   Error management of the unique contraint of a user
        while self.get_dao().get_folder_by_username():
            user_name = input(f"[ERROR] : the username {user_name} is arleady taken, please retry : ")
            self.get_dao().set_username_folder(user_name)

        #   Correct the paths for each file that must be created with the new username
        self.get_dao().set_absolute_paths()
        self.get_dao().create_db()

        user_master_password = getpass("\nEnter your master password: ")
        user_master_password_again = getpass("\nEnter your master password again: ")
        while user_master_password != user_master_password_again:
            print("Passwords do not match. Please try again.")
            user_master_password = getpass("\nEnter your master password again: ")
            user_master_password_again = getpass("\nEnter your master password again: ")
        #   Encrypt databases files with master password
        self.get_encryption_manager().set_master_password(user_master_password)  # Set once
        self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
        self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)

        #   Create a user object
        user = UserModel(user_name, user_master_password)

        #   Establishing connection to the DB is done in this method to be regroup frequent use of the 'connect' method
        self.get_dao().create_user(user)
        self.get_dao().close()

        #   Encrypt databases files with master password
        EncryptionModel.encrypt_db(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME, user_master_password, self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
        EncryptionModel.encrypt_db(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME, user_master_password, self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)
        input("Press Enter to go back to the main menu.")


    def connect_login(self):
        print("\n--------Connect to your login account--------")
        user_name = input("Enter your username/email: ")
        while not user_name:
            user_name = input("[ERROR] Please, Enter your username/email: ")

        self.set_dao(DAO(user_name))

        try:
            #   Ask for password to unlock the database
            master_password_input = getpass("\nEnter your master password: ")
            #   Decrypt the database to a temporary file when needed
            EncryptionModel.decrypt_db(self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_USER_NAME, master_password_input, self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
            EncryptionModel.decrypt_db(self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME, master_password_input, self.get_dao().get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)
        except() as e:
            print("\nUser denied, invalid master password!\n")
            input("Press Enter to go back to the main menu.")
            return
            
        while self.get_dao().connect_db(DEFAULT_DB_USER_NAME) == False:
            self.get_dao().close()
            print("\n [ERROR]: User don't exist, please retry \n")
            user_name = input("Enter your username/email: ")
            self.set_dao(DAO(user_name))

        user_tuple = self.get_dao().get_user_by_username(user_name)

        #   Verify if the query is giving something otherwise ask for a username again by prompting an error
        while user_tuple is None :
            print("[ERROR] : No user was found with this username, please retry\n")
            user_name = input("Enter your username/email: ")
            user_tuple = self.get_dao().get_user_by_username(user_name)

        #   master password & verify it's authenticity and is veracity
        master_password_db = self.get_dao().get_fullhashed_master_password(user_name)
        data_hash_db = self.get_dao().get_hashing_data(user_name)
        try:
            if HashModel.verify_password(data_hash_db, master_password_input, master_password_db):
                print("\nUser verified !\n")
                #   Set the password to encrypt databases
                self.get_encryption_manager().set_master_password(master_password_input)  # Set once
                self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME)
                self.get_encryption_manager().add_db_path(self.daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME)
                #   Launch the user menu controller
                self.set_user_master_password(master_password_input)
                self.get_dao().close()
                UserMenuController(self,  self.encryption_manager, user_name, self.get_dao()).run()
                self.running = False
            else :
                print("\nUser denied!\n")
            input("Press Enter to go back to the main menu.")
        except Exception as e:
            print("\n[Exception]!", str(e))


def encrypt_on_exit(daoConnect, user_master_password):
    if user_master_password is not None:
        print('\n\n[EXIT] Encrypting your database!\n')
        EncryptionModel.encrypt_db(
            daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME,
            user_master_password,
            daoConnect.get_path_to_db() + "/" + DEFAULT_DB_USER_NAME
        )
        EncryptionModel.encrypt_db(
            daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME,
            user_master_password,
            daoConnect.get_path_to_db() + "/" + DEFAULT_DB_PASSWORD_NAME
        )


if __name__ == "__main__":
    controller = MainController()  # Create an instance of MainController
    controller.run()  # Call the main menu method to start the program