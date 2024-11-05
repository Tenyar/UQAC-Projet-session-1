import shutil
import os
import view.UserMenuView as userView
import utility.functionUtility as functionUtility

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
    def __init__(self, mainController, username, dao):
        self.username = username
        self.mainController = mainController
        self.running = True
        self.userView = userView
        self.daoConnect = dao


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
                    self.delete_account()
                case 4:
                    self.disconnect()
                case 5:
                    self.exit()
                case _:
                    print("\n******************************\nInvalid option. Please try again.\n*******************************")


    def delete_account(self):
        print("\n--------------------------------------------------------")
        # Prompt for user confirmation
        self.daoConnect.close()
        
        user_choice = functionUtility.get_boolean_input("Would you like to suppress your account (Yes/no): ")
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  #    Climb up one level to reach the root
        folder_path = os.path.join(project_root, 'model', 'database', self.username)
        # Print the folder path for verification
        print(f"Folder path to delete: {folder_path}")
        
        print("Folder exists:", os.path.exists(folder_path))
        
        # Check if folder exists before trying to delete it
        if user_choice:
            if os.path.exists(folder_path):
                try:
                    # Use shutil.rmtree to delete the folder and all contents
                    shutil.rmtree(folder_path)
                    print("Account folder and contents successfully deleted.")
                except Exception as e:
                    print(f"Error while deleting folder: {e}")
            else:
                print("Folder not found, nothing to delete.")
        self.disconnect()


    def disconnect(self):
        self.running = False
        self.mainController.run()


    def exit(self):
        self.running = False