import hashlib
import argon2
import sys
import os

from model.HashModel import HashModel

#sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from model.DAO import DAO


class UserModel:
    def __init__(self, username, master_password):
        self.username = username
        
        #   Create variables to store password hashing parameters
        #   Also making it easier to read in the DAO class
        # !! since it's now an array of variables it's depreciated
        # self.algorithm = None
        # self.version = None
        # self.memory_cost = None
        # self.time_cost = None
        # self.parallelism = None
        # self.salt = None
        # self.hash_len = None
        # self.salt_len = None
        self.hash_params = {
        "algorithm" : None,
        "version" : None,
        "memory_cost" : None,
        "time_cost" : None,
        "parallelism" : None,
        "salt" : None,
        "hash_len" : None,
        "salt_len" : None,
        "hash" : None
        }
        
        #   Make it an array of parameters for the hashed password (easier to store in DB)
        print(master_password)
        #   Dissociate the full hash produced by the function from the list of parameters
        self.full_hash_value = HashModel.hash_password(master_password, self)

        #   Store variable from the hashed password to these variables
        HashModel.split_password(self.hash_params, self.full_hash_value)
        print("full_hash_value : ", self.full_hash_value)
    

    def set_username(self, username):
        self.username = username
