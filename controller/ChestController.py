import view.ChestView as chestView
import UserMenuController

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from model.DAO import DAO
class ChestController:
    def __init__(self, UserMenuController, username):
        self.UserMenuController =UserMenuController
        self.username = username
        self.running = True
        self.chest_view = chestView
        self.daoConnect = DAO(username)
        self.daoConnect.close()


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
        print(f"\n--------- All available passwords of [{self.username}] for different service ---------\n")
        self.daoConnect.connect_db(DEFAULT_DB_USER_NAME)
        password_list = self.daoConnect.get_all_user_service_password(self.username)
        # Iterate over each tuple and print it in dictionary format
        for service, password in password_list:
            print(f"---> Service: {service}, Password: {password}")
        print("\n--------- END ---------\n")
        

    def find_user_password(self):
        print(f"\n--------- Password of [{self.username}] for a service ---------\n")
        self.daoConnect.connect_db(DEFAULT_DB_USER_NAME)

        print("\n----\----\ [List of services] ----\----\n")
        all_services = self.daoConnect.get_all_services(self.username)
        for service in all_services:
            print(f"Service: {service[0]}")
        
        service_wanted = input("\nWhich service do you want to see the password of ?: ")

        password_list = self.daoConnect.get_user_service_password(self.username, service_wanted)
        for service, password in password_list:
            print(f"---> Service: {service}, Password: {password}")

        print("\n--------- END ---------\n")


    def go_back(self):
        self.running = False
        UserMenuController.run()


    def exit(self):
        self.running = False