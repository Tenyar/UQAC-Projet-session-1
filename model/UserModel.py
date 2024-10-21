import hashlib
import argon2
import sys
import os

#sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from model.DAO import DAO

# defaults constant of minimum limits (reasonable ones) for at least security with the hash
# Also default and minimum/maximum limits for security
DEFAULT_TIME_COST = 3
MIN_TIME_COST = 1
MAX_TIME_COST = 10  # Maximum time cost

DEFAULT_MEMORY_COST = 65536  # 64 MB
MIN_MEMORY_COST = 8192  # 8 MB
MAX_MEMORY_COST = 1048576  # 1 GB (in KiB)

DEFAULT_PARALLELISM = 4
MIN_PARALLELISM = 1
MAX_PARALLELISM = 8  # Max parallelism, use reasonable limits based on CPU cores

DEFAULT_HASH_LEN = 32
MIN_HASH_LEN = 16
MAX_HASH_LEN = 64  # Max length of the hash

DEFAULT_SALT_LEN = 16
MIN_SALT_LEN = 8
MAX_SALT_LEN = 32  # Max length of the salt

class UserModel:
    def __init__(self, username, master_password):
        self.username = username
        
        #   Create variables to store password hashing parameters
        #   Also making it easier to read in the DAO class
        self.algorithm = None
        self.version = None
        self.memory_cost = None
        self.time_cost = None
        self.parallelism = None
        self.salt = None
        self.hash_len = None
        self.salt_len = None
#       self.hash_password = None

        #   Make it an array of parameters for the hashed password (easier to store in DB)
        self.full_hash_value = self.hash_password(master_password)
        print("full_hash_value : ", self.full_hash_value)

        #   Store variable from the hashed password to these variables
        self.split_password()

        #self.daoConnect = DAO()
        #self.save_user()

    def hash_password(self, password):
            # Ask user personnal choices for hashing parameters
            # Use Argon2 to hash the master password (Argon2id would be better to prevent further breach)
            params = self.get_user_inputs()  # Ensure this method is defined
            print(params, "\n")
            # Verify if the values are correct for at least a minimum of security
            validated_params = self.validate_params(params)

            for x in validated_params:
                print("VALIDATING PARAMS:", validated_params[x])
            print("\n")
                
            # Use Argon2 to hash the master password with validated parameters
            ph = argon2.PasswordHasher(
                time_cost=validated_params["time_cost"],
                memory_cost=validated_params["memory_cost"],
                parallelism=validated_params["parallelism"],
                hash_len=validated_params["hash_len"],
                salt_len=validated_params["salt_len"]
            )
            return ph.hash(password)
        
    def get_user_inputs(self):
    #   Prompt user for all hash parameters and return them as a dictionary.
        # ---  means the algorithm takes time to run, making brute-forcing slower.
        time_cost = input("Enter time cost: ")
        # ---  ensures that an attacker would need significant memory to compute the hash.
        memory_cost = input("Enter memory cost (in KiB): ")
        # ---  allows for efficient use of CPU cores for legitimate users, but an attacker would need a lot of CPU power to brute-force.
        parallelism = input("Enter parallelism of the hash: ")
        hash_len = input("Enter hash length: ")
        salt_len = input("Enter salt length: ")

        # Store data about hashing
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len

        return {
            "time_cost": time_cost,
            "memory_cost": memory_cost,
            "parallelism": parallelism,
            "hash_len": hash_len,
            "salt_len": salt_len,
        }
    
    def validate_params(self, params):
    #   Validate all hash parameters at once.
        validated_params = {}
        
        # Ensure time cost is within the range of minimum and maximum limits
        validated_params["time_cost"] = max(
            min(int(params["time_cost"]) if params["time_cost"] else DEFAULT_TIME_COST, MAX_TIME_COST), MIN_TIME_COST
        )

        # Ensure memory cost is within the range of minimum and maximum limits
        validated_params["memory_cost"] = max(
            min(int(params["memory_cost"]) if params["memory_cost"] else DEFAULT_MEMORY_COST, MAX_MEMORY_COST), MIN_MEMORY_COST
        )

        # Ensure parallelism is within the range of minimum and maximum limits
        validated_params["parallelism"] = max(
            min(int(params["parallelism"]) if params["parallelism"] else DEFAULT_PARALLELISM, MAX_PARALLELISM), MIN_PARALLELISM
        )

        # Ensure hash length is within the range of minimum and maximum limits
        validated_params["hash_len"] = max(
            min(int(params["hash_len"]) if params["hash_len"] else DEFAULT_HASH_LEN, MAX_HASH_LEN), MIN_HASH_LEN
        )

        # Ensure salt length is within the range of minimum and maximum limits
        validated_params["salt_len"] = max(
            min(int(params["salt_len"]) if params["salt_len"] else DEFAULT_SALT_LEN, MAX_SALT_LEN), MIN_SALT_LEN
        )
        
        #   Store these values in the instance variables
        self.time_cost = validated_params["time_cost"]
        self.memory_cost = validated_params["memory_cost"]
        self.parallelism = validated_params["parallelism"]
        self.hash_len = validated_params["hash_len"]
        self.salt_len = validated_params["salt_len"]
        
        return validated_params
    
    # ? Peut on mettre cette méthode en static pour être utilitaire à d'autre mdp comme ceux des sites ? (évite d'en avoir deux)
    def split_password(self):
        print("entering split Password : ", self.full_hash_value)
        # Step 1: delete "$" symbol and divide the string
        parts = self.full_hash_value.split('$')

        # Ignore the first empty element (because it's empty)
        parts = parts[1:]

        #print(parts)
        # Get the different parts
        self.algorithm  = parts[0]  # 'argon2id'
        self.version = parts[1].split('=')[1]

        # Step 2: divide parameters (m=...,t=...,p=...)
        params = parts[2].split(',')

        self.memory_cost = params[0].split('=')[1]
        self.time_cost = params[1].split('=')[1]
        self.parallelism = params[2].split('=')[1]

        # Step 3: Extract salt & hash
        self.salt = parts[3]
        self.hash_password = parts[4]

        # ? Afficher les résultats pour le moments. (à enlever car WIP)
        print("Algorithm:", self.algorithm)
        print("Version:", self.version)
        print("Memory Cost:", self.memory_cost)
        print("Time Cost:", self.time_cost)
        print("Parallelism:", self.parallelism)
        print("Salt:", self.salt)
        print("Hash_len:", self.hash_len)
        print("salt_len:", self.salt_len)
        print("Hash:", self.hash_password)

    # !!!! DEMANDER SI C'EST BON
#   def save_user(self):
#       try:
#           # Logic to save the user to a database (SQLite)
#           self.daoConnect.connect()
#           self.daoConnect.create_user()
#       except ValueError:
#                print("\n******************************\nException ! an odd error might occured during the save of user\n******************************")