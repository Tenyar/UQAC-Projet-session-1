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
        self.generate_model = GeneratorModel()
        self.daoConnect = DAO(username)
        self.daoConnect.close()


    def create_password(self, gen_values):
        #   Create a password for an account or other
        password_generated = self.generate_model.generate_password(gen_values)
        print("Generated password", password_generated)
        return password_generated
    

    def get_generator_model(self):
        return self.generate_model

    
    def password_to_db(self, service_name, password_generated):
        self.daoConnect.connect_db()
        self.daoConnect.create_user_passwords(self.username, service_name, password_generated)
        self.daoConnect.close()


    def go_back(self):
        self.running = False
        self.UserMenuController.run()


    def exit(self):
        self.running = False