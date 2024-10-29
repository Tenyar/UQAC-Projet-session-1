import view.ChestView as chestView
import UserMenuController

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
class ChestController:
    def __init__(self, UserMenuController, username):
        self.UserMenuController =UserMenuController
        self.username = username
        self.running = True
        self.chest_view = chestView
        self.daoConnect = None

    def run(self):
        while self.running:
            self.chest_view.display_chest_view()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                    self.show_all_user_passwords() # Call the controller of that page
                case 2:
                    self.find_user_password()
                case 3:
                    self.go_back() 
                case 4:
                    self.exit()
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def show_all_user_passwords(self):
        print("\n--------- All available passwords for different service ---------\n")

    def find_user_password(self):
        print("\n--------- Password for a service ---------\n")



    def go_back(self):
        self.running = False
        UserMenuController.run()


    def exit(self):
        self.running = False