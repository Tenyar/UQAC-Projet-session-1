import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from argon2.low_level import hash_secret_raw, Type
from cryptography.exceptions import InvalidSignature


#   Base path for the project
BASE_PATH = "base_path/project/model/database/"


class EncryptionModel:
    #   Define a unique header for encrypted files
    ENCRYPTED_HEADER = b"ENCRYPTED" 

    def derive_key(password: str, salt: bytes) -> bytes:
        #   derive a 32 bytes key (256 bits) using Argon2id
        return hash_secret_raw(
            password.encode(),
            salt,
            time_cost=2,        # Number of iterations (peut être ajusté)
            memory_cost=102400, # Memory in KB (100MB here)
            parallelism=8,      # Number of threads (can be adjusted)
            hash_len=32,        # Size of derived key
            type=Type.ID        # Use Argon2id
        )
    

    @staticmethod
    def encrypt_db(input_file: str, password: str, output_file: str):
        #   Check if the file is already encrypted
        with open(input_file, 'rb') as f:
            #   Read the file in binary mode until the length of the header
            header = f.read(len(EncryptionModel.ENCRYPTED_HEADER))
            if header == EncryptionModel.ENCRYPTED_HEADER:
                #   print(f"{input_file} is already encrypted. Skipping encryption.")
                return  #   Skip encryption if header is present
            
        # Generate salt, iv, and derive encryption key as usual
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = EncryptionModel.derive_key(password, salt)
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Read plaintext, pad it, and encrypt
        with open(input_file, 'rb') as f:
            plaintext = f.read()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Write encrypted header, salt, iv, and ciphertext to the output file
        with open(output_file, 'wb') as f:
            f.write(EncryptionModel.ENCRYPTED_HEADER)  # Write header
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)
        # print(f"{input_file} has been encrypted and saved to {output_file}.")


    @staticmethod
    def decrypt_db(encrypted_file: str, password: str, output_file: str):
        try:
            with open(encrypted_file, 'rb') as f:
                # Check for header
                header = f.read(len(EncryptionModel.ENCRYPTED_HEADER))
                if header != EncryptionModel.ENCRYPTED_HEADER:
                    print("Error: File is not properly encrypted or missing header.")
                    return False
                
                # Read salt, IV, and ciphertext
                salt = f.read(16)
                iv = f.read(16)
                ciphertext = f.read()
            
            # Derive the key
            key = EncryptionModel.derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Attempt decryption
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_data) + unpadder.finalize()

            # Write the decrypted plaintext to the output file
            with open(output_file, 'wb') as f:
                f.write(plaintext)

            return True

        except (ValueError, InvalidSignature) as e:
            print("Error: Incorrect password or failed decryption.")
            return False