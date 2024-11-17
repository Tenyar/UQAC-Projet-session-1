import argon2

#   Importing usefull constants
# Importing time cost constants
from utility.ConstantsUtility import (
    DEFAULT_TIME_COST, MIN_TIME_COST, MAX_TIME_COST
)

# Importing memory cost constants
from utility.ConstantsUtility import (
    DEFAULT_MEMORY_COST, MIN_MEMORY_COST, MAX_MEMORY_COST
)

# Importing parallelism constants
from utility.ConstantsUtility import (
    DEFAULT_PARALLELISM, MIN_PARALLELISM, MAX_PARALLELISM
)

# Importing hash length constants
from utility.ConstantsUtility import (
    DEFAULT_HASH_LEN, MIN_HASH_LEN, MAX_HASH_LEN
)

# Importing salt length constants
from utility.ConstantsUtility import (
    DEFAULT_SALT_LEN, MIN_SALT_LEN, MAX_SALT_LEN
)

#   Utility class for hashing functions
class HashModel:
    def __init__(self,):
        #    self.full_hash_value = full_hash_value
        #    self.ph = argon2.PasswordHasher()  # Initialize PasswordHasher
        return


    def get_user_inputs():
        #   Prompt user for all hash parameters and return them as a dictionary.
        # ---  means the algorithm takes time to run, making brute-forcing slower.
        time_cost = input("Enter time cost: ")
        # ---  ensures that an attacker would need significant memory to compute the hash.
        memory_cost = input("Enter memory cost (in KiB): ")
        # ---  allows for efficient use of CPU cores for legitimate users, but an attacker would need a lot of CPU power to brute-force.
        parallelism = input("Enter parallelism of the hash: ")
        hash_len = input("Enter hash length: ")
        salt_len = input("Enter salt length: ")

        return {
            "time_cost": time_cost,
            "memory_cost": memory_cost,
            "parallelism": parallelism,
            "hash_len": hash_len,
            "salt_len": salt_len,
        }
    

    @staticmethod
    def hash_password(password: str, user=None):
        # Ask user personnal choices for hashing parameters
        # Use Argon2 to hash the master password (Argon2id would be better to prevent further breach)
        hash_params = HashModel.get_user_inputs()
        print(hash_params, "\n")
        # Verify if the values are correct for at least a minimum of security
        validated_hash_params = HashModel.validate_hashed_params(hash_params)

        # Store data about hashing
        if user:
            user.hash_params["time_cost"] = validated_hash_params["time_cost"]
            user.hash_params["memory_cost"] = validated_hash_params["memory_cost"]
            user.hash_params["parallelism"] = validated_hash_params["parallelism"]
            user.hash_params["hash_len"] = validated_hash_params["hash_len"]
            user.hash_params["salt_len"] = validated_hash_params["salt_len"]

        for x,y in validated_hash_params.items():
            print(f"VALIDATING PARAMS FOR {x} :", {y})
        print("\n")
            
        # Use Argon2 to hash the master password with validated parameters
        ph = argon2.PasswordHasher(
            time_cost=validated_hash_params["time_cost"],
            memory_cost=validated_hash_params["memory_cost"],
            parallelism=validated_hash_params["parallelism"],
            hash_len=validated_hash_params["hash_len"],
            salt_len=validated_hash_params["salt_len"]
        )
        return ph.hash(password)


    @staticmethod
    #   hash_data = all elements used during the hashing of the password
    def verify_password(hash_data: dict, input_password: str, db_password: str):
        print(hash_data)
        try:
            ph = argon2.PasswordHasher(
                time_cost = hash_data["time_cost"],
                memory_cost = hash_data["memory_cost"],
                parallelism = hash_data["parallelism"],
                hash_len = int(hash_data["hash_len"]),
                salt_len = int(hash_data["salt_len"])
            )
            # The correct usage should be to verify the input_password against the db_password
            ph.verify(db_password, input_password)  
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
    

    def validate_hashed_params(hash_params: dict):
    #   Validate all hash parameters at once.
        validated_params = {}
        
        # Ensure time cost is within the range of minimum and maximum limits
        validated_params["time_cost"] = max(
            min(int(hash_params["time_cost"]) if hash_params["time_cost"] else DEFAULT_TIME_COST, MAX_TIME_COST), MIN_TIME_COST
        )

        # Ensure memory cost is within the range of minimum and maximum limits
        validated_params["memory_cost"] = max(
            min(int(hash_params["memory_cost"]) if hash_params["memory_cost"] else DEFAULT_MEMORY_COST, MAX_MEMORY_COST), MIN_MEMORY_COST
        )

        # Ensure parallelism is within the range of minimum and maximum limits
        validated_params["parallelism"] = max(
            min(int(hash_params["parallelism"]) if hash_params["parallelism"] else DEFAULT_PARALLELISM, MAX_PARALLELISM), MIN_PARALLELISM
        )

        # Ensure hash length is within the range of minimum and maximum limits
        validated_params["hash_len"] = max(
            min(int(hash_params["hash_len"]) if hash_params["hash_len"] else DEFAULT_HASH_LEN, MAX_HASH_LEN), MIN_HASH_LEN
        )

        # Ensure salt length is within the range of minimum and maximum limits
        validated_params["salt_len"] = max(
            min(int(hash_params["salt_len"]) if hash_params["salt_len"] else DEFAULT_SALT_LEN, MAX_SALT_LEN), MIN_SALT_LEN
        )
        
        return validated_params
    

    # ? Peut on mettre cette méthode en static pour être utilitaire à d'autre mdp comme ceux des sites ? (évite d'en avoir deux)
    def split_password(hash_params, full_hashed_value):
        print("entering split Password : ", full_hashed_value)
        # Step 1: delete "$" symbol and divide the string
        parts = full_hashed_value.split('$')

        # Ignore the first empty element (because it's empty)
        parts = parts[1:]

        #print(parts)
        # Get the different parts
        hash_params["algorithm"]  = parts[0]  # 'argon2id'
        hash_params["version"] = parts[1].split('=')[1]

        # Step 2: divide parameters (m=...,t=...,p=...)
        params = parts[2].split(',')

        hash_params["memory_cost"] = params[0].split('=')[1]
        hash_params["time_cost"] = params[1].split('=')[1]
        hash_params["parallelism"] = params[2].split('=')[1]

        # Step 3: Extract salt & hash
        hash_params["salt"] = parts[3]
        hash_params["hash_password"] = parts[4]

        # ? Afficher les résultats pour le moments. (à enlever car WIP)
        print("Algorithm:", hash_params["algorithm"])
        print("Version:", hash_params["version"])
        print("Memory Cost:", hash_params["memory_cost"])
        print("Time Cost:", hash_params["time_cost"])
        print("Parallelism:", hash_params["parallelism"])
        print("Salt:", hash_params["salt"])
        print("Hash_len:", hash_params["hash_len"])
        print("Salt_len:", hash_params["salt_len"])
        print("Hash:", hash_params["hash_password"])