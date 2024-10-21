import hashlib
import argon2
import sys
import os

#   Utility class for hashing functions

class HashModel:
    def __init__(self,):
        #    self.full_hash_value = full_hash_value
        #    self.ph = argon2.PasswordHasher()  # Initialize PasswordHasher
        return

    @staticmethod
    #   hash_data = all elements used during the hashing of the password
    def verify_password(hash_data, input_password, db_password):
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