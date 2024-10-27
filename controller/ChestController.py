import sys
import os

import view.ChestView as chestView
import UserMenuController

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
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
class ChestController:
    def __init__(self):
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
                    self.generate_password() # Call the controller of that page
                case 2:
                    self.go_back() # Call the instance method
                case 3:
                    self.exit() # Call the instance method
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")

    def generate_password(self):
        print('*******  Generating a new password  *******')
        password_chosen = None
        password_length = None   # 8 - 128 characters
        lowercase_alphabet=False    # a-z
        uppercase_alphabet=False    # a-Z
        numbers=False  #0-9



    def go_back(self):
        self.running = False
        UserMenuController.run()

    def exit(self):
        self.running = False