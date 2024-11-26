from model.EncryptionModel import EncryptionModel
from utility.ViewFunctionsUtility import ViewFunctionsUtility

class EncryptionManager:
    def __init__(self):
        self.db_paths = []
        #self.master_password = None


    def add_db_path(self, db_path):
        if db_path not in self.db_paths:
            self.db_paths.append(db_path)


    def encrypt_on_exit(self, password):
        # Retrieve the entered password
        if password:
            print('\n\n[EXIT] Encrypting your database(s)!\n')
            for db_path in self.db_paths:
                encrypted_path = db_path
                EncryptionModel.encrypt_db(db_path, password, encrypted_path)
            return True
            #    print(f"Encrypted {db_path} to {encrypted_path}")
        return False