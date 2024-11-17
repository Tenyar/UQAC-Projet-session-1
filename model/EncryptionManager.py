from model.EncryptionModel import EncryptionModel

class EncryptionManager:
    def __init__(self):
        self.db_paths = []
        self.master_password = None


    def set_master_password(self, password):
        self.master_password = password


    def add_db_path(self, db_path):
        if db_path not in self.db_paths:
            self.db_paths.append(db_path)


    def encrypt_on_exit(self):
        if self.master_password:
            print('\n\n[EXIT] Encrypting your database(s)!\n')
            for db_path in self.db_paths:
                encrypted_path = db_path # + ".enc"
                EncryptionModel.encrypt_db(db_path, self.master_password, encrypted_path)
            #    print(f"Encrypted {db_path} to {encrypted_path}")