import sys
import os

import view.GeneratorView as generatorView
from model.GeneratorModel import GeneratorModel

from model.DAO import DAO
#####################################################################################
#          #######      #               ##########
#        #              #                   #
#       #               #                   #
#       #               #                   #           (command line interface)
#        #              #                   #
#          #######      ########        ##########
#####################################################################################
class GeneratorController:
    def __init__(self, UserMenuController, username):
        self.UserMenuController = UserMenuController
        self.running = True
        self.generator_view = generatorView
        self.generateModel = GeneratorModel(username)
        self.daoConnect = None


    def run(self):
        while self.running:
            self.generator_view.display_generator_view()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                    print("Generated password", self.generateModel.generate_password()) # Call the controller of that page
                case 2:
                    self.go_back() 
                case 3:
                    self.exit() 
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def go_back(self):
        self.running = False
        self.UserMenuController.run()


    def exit(self):
        self.running = False