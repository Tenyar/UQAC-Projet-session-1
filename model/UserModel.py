import hashlib
import argon2

from model.DAO import DAO

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
        self.hashed_password = self.hash_password(master_password)
        print(self.username)
        print('Hashed Password :', self.hashed_password)

    def hash_password(self, password):
        # Ask user personnal choices for hashing parameters
        # Use Argon2 to hash the master password (Argon2id would be better to prevent further breach)
        params = self.get_user_inputs()
        # Verify if the values are correct for at least a minimum of security
        validated_params = self.validate_params(params)

        for x in validated_params:
            print(validated_params[x])
        # Use Argon2 to hash the master password with validated parameters
        ph = argon2.PasswordHasher(
            time_cost = validated_params["time_cost"],
            memory_cost = validated_params["memory_cost"],
            parallelism = validated_params["parallelism"],
            hash_len = validated_params["hash_len"],
            salt_len = validated_params["salt_len"]
        )
        return ph.hash(password)

    def get_user_inputs(self):
    #   Prompt user for all hash parameters and return them as a dictionary.
        params = {
        # ---  means the algorithm takes time to run, making brute-forcing slower.
            "time_cost": input("\nEnter the time cost of the hash: "),
        # ---  ensures that an attacker would need significant memory to compute the hash.
            "memory_cost": input("\nEnter the memory cost of the hash (in KiB): "),
        # ---  allows for efficient use of CPU cores for legitimate users, but an attacker would need a lot of CPU power to brute-force.
            "parallelism": input("\nEnter the parallelism of the hash: "),
            "hash_len": input("\nEnter the length of the hash: "),
            "salt_len": input("\nEnter the length of the salt: ")
        }
        return params
    
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

        return validated_params

    def verify_password(self, input_password):
        # ---  Verify the input password by comparing the hash
        ph = argon2.PasswordHasher()
        try:
            ph.verify(self.hashed_password, input_password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        
    # !!!! DEMANDER SI C'EST BON
    def save_user(self, db_connection):
        # Logic to save the user to a database (SQLite)
        cursor = db_connection.cursor()
        cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                       (self.username, self.hashed_password))
        db_connection.commit()