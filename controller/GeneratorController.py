import sys
import os

import view.GeneratorView as generatorView
import UserMenuController

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
class GeneratorController:
    def __init__(self):
        self.running = True
        self.generator_view = generatorView
        self.daoConnect = None

    def run(self):
        while self.running:
            self.generator_view.displaygenerator_view()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                    print("Generated password", self.generate_password()) # Call the controller of that page
                case 2:
                    self.go_back() # Call the instance method
                case 3:
                    self.exit() # Call the instance method
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")

    def go_back(self):
        self.running = False
        UserMenuController.run()

    def exit(self):
        self.running = False