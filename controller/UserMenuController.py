import sys
import os

import view.UserMenuView as userView
import ChestController
import GeneratorController

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
#####################################################################################
#          #######      #               ##########
#        #              #                   #
#       #               #                   #
#       #               #                   #           (command line interface)
#        #              #                   #
#          #######      ########        ##########
#####################################################################################
class UserMenuController:
    def __init__(self, mainController):
        self.mainController = mainController
        self.running = True
        self.userView = userView
        self.daoConnect = None

    def run(self):
        while self.running:
            self.userView.user_main_menu()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                    GeneratorController() # Call the controller of that page
                case 2:
                    ChestController()
                case 3:
                    self.disconnect() # Call the instance method
                case 4:
                    self.exit() # Call the instance method
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")

    def disconnect(self):
        self.running = False
        self.mainController.run()

    def exit(self):
        self.running = False