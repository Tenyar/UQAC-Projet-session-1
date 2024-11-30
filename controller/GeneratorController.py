import sys
import os


from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from model.GeneratorModel import GeneratorModel
from model.DAO import DAO

class GeneratorController:
    def __init__(self, UserMenuController, username):
        self.username = username
        self.UserMenuController = UserMenuController
        self.running = True
        self.generateModel = GeneratorModel(username)
        self.daoConnect = DAO(username)
        self.daoConnect.close()


    def create_password(self, gen_values):
        #   Create a password for an account or other
        password_generated = self.generateModel.generate_password(gen_values)
        print("Generated password", password_generated)
        return password_generated
    
    
    def password_to_db(self, service_name, password_generated):
        print(service_name)
        print(service_name)
        self.daoConnect.connect_db()
        self.daoConnect.create_user_passwords(self.username, service_name, password_generated)


    def go_back(self):
        self.running = False
        self.UserMenuController.run()


    def exit(self):
        self.running = False