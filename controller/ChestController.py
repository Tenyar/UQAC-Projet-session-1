import UserMenuController

from model.DAO import DAO
class ChestController:
    def __init__(self, UserMenuController, username):
        self.UserMenuController =UserMenuController
        self.username = username
        self.running = True
        self.daoConnect = DAO(username)
        self.daoConnect.close()


    def show_all_user_passwords(self):
        self.daoConnect.connect_db()
        password_list = self.daoConnect.get_all_user_service_password(self.username)
        self.daoConnect.close()
        return password_list
        

    def delete_service(self, username, service_name, password):
        self.daoConnect.connect_db()
        if self.daoConnect.delete_service(username, service_name, password):
            self.daoConnect.close()
            return True
        self.daoConnect.close()
        return False


    def find_user_password(self):
        self.daoConnect.connect_db()
        all_services = self.daoConnect.get_all_services(self.username)
        for service in all_services:
            print(f"Service: {service[0]}")
        
        service_wanted = input("\nWhich service do you want to see the password of ?: ")
        password_list = self.daoConnect.get_user_service_password(self.username, service_wanted)
        for service, password in password_list:
            print(f"---> Service: {service}, Password: {password}")
        self.daoConnect.close()


    def go_back(self):
        self.running = False
        UserMenuController.run()


    def exit(self):
        self.running = False