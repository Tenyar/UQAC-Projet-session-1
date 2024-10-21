import sys
import os

# Add the project root directory to sys.path (for importing custom classes)
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import view.MainView as MainView

from model.DAO import DAO
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
        self.mainView = MainView
        self.daoConnect = DAO()

    def main_menu(self):
        while True:
            self.mainView.mainMenu()  # Call the utility function to display the menu
            try:
                choice = int(input("\nEnter your choice: "))  # Convert input to int
                print('Your choice:', choice)
                match choice:
                    case 1:
                        self.create_login()  # Call the instance method
                    case 2:
                        self.connect_login()  # Call the instance method
                    case 3:
                        self.exit_program()  # Call the instance method
                    case _:
                        print("\n******************************\nInvalid option. Please try again.\n*******************************")
            except ValueError:
                print("\n******************************\nException ! an odd error might occured\n******************************")

    def create_login(self):
        print("Creating a new login")
        user_name = input("\nEnter your name/email: ")  # User's name/email
        user_main_password = getpass("\nEnter your main password: ")
        user_main_password_again = getpass("\nEnter your main password again: ")

        while user_main_password != user_main_password_again:
            print("Passwords do not match. Please try again.")
            user_main_password = getpass("\nEnter your main password: ")
            user_main_password_again = getpass("\nEnter your main password again: ")
        
        # Implement hashing and storing logic here (using self.model)
        # For example: password_hash = hashlib.sha512(user_main_password.encode('utf-8')).hexdigest()
        user = UserModel(user_name, user_main_password) # --- Pepper use cases.
        print(user.full_hash_value)
        # Establish connection to DB
        self.daoConnect.connect()
        self.daoConnect.create_user(user)
        input("Press Enter to go back to the main menu.")

    def connect_login(self):
        print("Connect to your login account")
        # Implement logic for connecting to an account here...
        self.DaoConnect.connect()

        input("Press Enter to go back to the main menu.")

    def exit_program(self):
        print("Exiting the program...")
        sys.exit(0)

if __name__ == "__main__":
    controller = MainController()  # Create an instance of MainController
    controller.main_menu()  # Call the main menu method to start the program