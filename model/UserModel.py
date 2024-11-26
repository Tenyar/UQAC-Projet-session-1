import hashlib
import argon2
import sys
import os

from model.HashModel import HashModel

#sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from model.DAO import DAO


class UserModel:
    def __init__(self, username, master_password, hash_params):
        self.username = username
        
        #   Create variables to store password hashing parameters
        #   Also making it easier to read in the DAO class
        # !! since it's now an array of variables it's depreciated
        #   Make it an array of parameters for the hashed password (easier to store in DB)
        self.hash_params = hash_params
        self.hash_params["algorithm"] = None
        self.hash_params["version"] = None
        self.hash_params["salt"] = None
        self.hash_params["hash"] = None
        
        #   Dissociate the full hash produced by the function from the list of parameters
        self.full_hash_value = HashModel.hash_password(master_password, hash_params, self)

        #   Store variable from the hashed password to these variables
        HashModel.split_password(self.hash_params, self.full_hash_value)
        print("full_hash_value : ", self.full_hash_value)
    

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username
    
    def get_full_hash_password(self):
        return self.full_hash_value
    
    def get_all_params(self):
        return self.hash_params

    def get_param(self, param):
        return self.hash_params[param]
    
    def set_param(self, param, value):
        self.hash_params[param] = value