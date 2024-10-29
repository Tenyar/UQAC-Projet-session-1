import sys
import os

# Add the project root directory to sys.path (for importing custom classes)
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import view.MainView as MainView

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from UserMenuController import UserMenuController
from model.DAO import DAO
from model.HashModel import HashModel
from getpass import getpass # Utility to hide inputs when writing a password
from model.UserModel import UserModel # Argond2(id) is used in this prototype for better security (longer time for hash)
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


    def run(self):
        while self.running:
            self.main_view.dispaly_main_menu()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
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
        self.daoConnect = DAO(user_name)

        #   Error management of the unique contraint of a user
        while self.daoConnect.get_folder_by_username():
            print(f"[ERROR] : the username {user_name} is arleady taken, please retry : ")
            user_name = input()
            self.daoConnect.set_username_folder(user_name)

        self.daoConnect.create_db()

        user_main_password = getpass("\nEnter your master password: ")
        user_main_password_again = getpass("\nEnter your master password again: ")
        while user_main_password != user_main_password_again:
            print("Passwords do not match. Please try again.")
            user_main_password = getpass("\nEnter your master password again: ")
            user_main_password_again = getpass("\nEnter your master password again: ")
        
        #   Create a user object
        user = UserModel(user_name, user_main_password)

        #   Establishing connection to the DB is done in this method to be regroup frequent use of the 'connect' method
        self.daoConnect.create_user(user)
        input("Press Enter to go back to the main menu.")


    def connect_login(self):
        print("\n--------Connect to your login account--------")
        # Implement logic for connecting to an account here...
        username_input = input("Enter your username/email: ")
        self.daoConnect = DAO(username_input)

        while self.daoConnect.connect_db(DEFAULT_DB_USER_NAME) == False:
            print("\n [ERROR]: User don't exist, please retry \n")
            username_input = input("Enter your username/email: ")
            self.daoConnect = DAO(username_input)

        user_tuple = self.daoConnect.get_user_by_username(username_input)

        #   Verify if the query is giving something otherwise ask for a username again by prompting an error
        while user_tuple is None :
            print("[ERROR] : No user was found with this username, please retry\n")
            username_input = input("Enter your username/email: ")
            user_tuple = self.daoConnect.get_user_by_username(username_input)
            
        #   Ask for master password & verify it's authenticity and is veracity
        master_password_input = getpass("\nEnter your master password: ")
        master_password_db = self.daoConnect.get_fullhashed_master_password(username_input)
        data_hash_db = self.daoConnect.get_hashing_data(username_input)

        try:
            if HashModel.verify_password(data_hash_db, master_password_input, master_password_db):
                print("\nUser verified !\n")
                # Launch the user menu controller
                UserMenuController(self, username_input).run()
                self.running = False
            else :
                print("\nUser denied!\n")

            input("Press Enter to go back to the main menu.")
        except Exception as e:
            print("\n[Exception]!", str(e))


if __name__ == "__main__":
    controller = MainController()  # Create an instance of MainController
    controller.run()  # Call the main menu method to start the program