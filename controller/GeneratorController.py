import sys
import os

import view.GeneratorView as generatorView

from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
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
        self.username = username
        self.UserMenuController = UserMenuController
        self.running = True
        self.generator_view = generatorView
        self.generateModel = GeneratorModel(username)
        self.daoConnect = DAO(username)
        self.daoConnect.close()


    def run(self):
        while self.running:
            self.generator_view.display_generator_view()  # Call the utility function to display the menu
            choice = int(input("\nEnter your choice: "))  # Convert input to int
            print('Your choice:', choice)
            match choice:
                case 1:
                     self.create_password()
                case 2:
                    self.go_back() 
                case 3:
                    self.exit() 
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def create_password(self):
        #   Create a password for an account or other
        print("For which service this password is for?")
        service_name = input()
        while not service_name:
            print('[ERROR] Please, enter a name for the service?')
            service_name = input()
            
        password_generated = self.generateModel.generate_password()
        print("Generated password", password_generated)
        self.daoConnect.connect_db(DEFAULT_DB_USER_NAME)
        self.daoConnect.create_user_passwords(self.username, service_name, password_generated)


    def go_back(self):
        self.running = False
        self.UserMenuController.run()


    def exit(self):
        self.running = False