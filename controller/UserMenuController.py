import sys
import os

import view.UserMenuView as userView

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from GeneratorController import GeneratorController
from ChestController import ChestController
#####################################################################################
#          #######      #               ##########
#        #              #                   #
#       #               #                   #
#       #               #                   #           (command line interface)
#        #              #                   #
#          #######      ########        ##########
#####################################################################################
class UserMenuController:
    def __init__(self, mainController, username):
        self.username = username
        self.mainController = mainController
        self.running = True
        self.userView = userView
        self.daoConnect = None


    def run(self):
        while self.running:
            self.userView.display_user_menu()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                    GeneratorController(self, self.username).run() # Call the controller of that page
                    self.running = False
                case 2:
                    ChestController(self, self.username).run()
                    self.running = False
                case 3:
                    self.disconnect()
                case 4:
                    self.exit()
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def disconnect(self):
        self.running = False
        self.mainController.run()


    def exit(self):
        self.running = False