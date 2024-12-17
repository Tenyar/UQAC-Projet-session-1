import sqlite3
import os

#   Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)
from model.HashModel import HashModel
#   For file encryption


class DAO:
    def __init__(self, username):
        #   Prepare the second DB for passwords
        self.db_password_name = DEFAULT_DB_PASSWORD_NAME
        #   Arbitrary name (until user can write a name for it)
        self.db_user_name = DEFAULT_DB_USER_NAME
        #   Path for checking if the file(DB) exist inside the app
        #   Variable that stores the database for a username
        self.username_folder = username
        self.path_to_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder)
        self.absolute_path_user = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder, self.db_user_name)
        self.absolute_path_password = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder, self.db_password_name)
        self.connection_pswd = None
        self.connection_user = None
        self.cursor = None
    

    def connect_db(self):
        try:
            #   Connect both databases
            self.connection_pswd = sqlite3.connect(self.absolute_path_password)
            self.connection_user = sqlite3.connect(self.absolute_path_user)

            self.cursor = self.connection_user.cursor()
            self.cursor = self.connection_pswd.cursor()

        except Exception as e:
            print("\n[Exception]!", str(e))
            return False


    def close(self):
        #   Close the database connection.
        if self.connection_pswd:
            print("Password database connection closed.")
            self.connection_pswd.close()
        if self.connection_user:
            print("User database connection closed.")
            self.connection_user.close()
        self.cursor = None

#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#   Creating the databases
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def create_db(self):
        #   Create the database in the "database/" folder
        #   Connect to the SQLite database. If it doesn't exist, it will be created.
        if not os.path.exists(self.absolute_path_password) and not os.path.exists(self.absolute_path_user):
            while(self.db_user_name == self.db_password_name):
                self.db_user_name = input("[ERROR] : the user DB can't have the same name as the 'password.db', please retry : \n")

            #   Create the folder for DB that is named after the username
            folder_path = os.path.dirname(self.absolute_path_user)
            if not os.path.exists(folder_path):
                print(f"Creating directory for user database at: {folder_path}")
                os.makedirs(folder_path)

            #   Formatting the name to be suited for creating a DB
            #   self.db_user_name = self.db_user_name + ".db"
            print(f"Database not found. Creating a new one at {"database", self.db_user_name}.")

            #   Create both databases
            self.connection_pswd = sqlite3.connect(self.absolute_path_password)
            self.connection_user = sqlite3.connect(self.absolute_path_user)

            self.create_passwords_tables()
            self.create_user_tables()


    def create_passwords_tables(self):
        #   Create the necessary tables if they don't exist.
        cursor = self.connection_pswd.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                username TEXT NOT NULL,
                full_hashed_password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PasswordData (
                username TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                version TEXT NOT NULL,
                memorycost INTEGER NOT NULL,
                timecost INTEGER NOT NULL,
                parallelism INTEGER NOT NULL,
                salt TEXT NOT NULL,
                hash_len TEXT NOT NULL,
                salt_len TEXT NOT NULL,
                split_hashed_password TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES User(username)
            )
        ''')
        self.connection_pswd.commit()


    def create_user_tables(self):
        self.get_db_cursor(DEFAULT_DB_USER_NAME)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserData (
                username TEXT NOT NULL,
                service_name TEXT NOT NULL,
                password TEXT NOT NULL
            ) 
        ''')
        self.connection_user.commit()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#   Getters
#   &
#   CRUD methods for databases
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #   Method to get the cursor for one of the connection to one of the 2 databases for a user.
    # Cursor = Variable switching between user and password db to provide a way to use sql query.
    def get_db_cursor(self, db_type: str):
        if(db_type == DEFAULT_DB_PASSWORD_NAME):
            self.cursor = self.connection_pswd.cursor()
        elif(db_type == DEFAULT_DB_USER_NAME):
            self.cursor = self.connection_user.cursor()


    #   Boolean, allows user to know if a database for a username exist
    def get_folder_by_username(self):
        username_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder)
        if (os.path.exists(username_folder_path)):
            return True
        return False


    #   Get the path where the database are
    def get_path_to_db(self):
        return self.path_to_db
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#   Password database
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #   Prepared request for safety (for sql)
    def get_user_by_username(self, username: str):
        try:
            # Prepared statement to get the user's details
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT * FROM User WHERE username = ?
            ''', (username,))
            
            user = self.cursor.fetchone()  # Fetch the result (None if no result) 
            
            if user:
                print(f"\nUser found: {user}\n")
            else:
                print(f"\nUser {username} not found.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
        return user


    def get_fullhashed_master_password(self, username: str):
        try:
            #   Query to retrieve master_password from MasterPassword table using username
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT full_hashed_password FROM User WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchone()

            if result:
                master_password = result[0]  # Extract the master_password from the result
                print(f"full_hashed_password for {username}: {master_password}\n")
                return master_password
            else:
                print(f"No full_hashed_password found for username: {username}\n")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


    def get_all_hashed_params(self, username: str):
        try:
         # Query to retrieve master_password from MasterPassword table using username
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT * FROM PasswordData WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchall()

            if result:
                #master_password = result[0]  # Extract the master_password from the result
                print(f"split_hashed_password for {username}: {result}\n")
                #   Transform the tuple into a dictionnary
                keys = ["username", "algo", "time_cost", "memory_cost", "parallelism", "salt_len", "salt", "hash_len", "hashed_password", "derived_key"]
                first_row = result[0]
                result_dict = dict(zip(keys, first_row))
                return result_dict
            else:
                print(f"No split_hashed_password found for username: {username}\n")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return None


    def get_hashed_master_password(self, username: str):
        try:
            # Query to retrieve master_password from MasterPassword table using username
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT split_hashed_password FROM PasswordData WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchone()

            if result:
                master_password = result[0]  # Extract the master_password from the result
                print(f"split_hashed_password for {username}: {master_password}\n")
                return master_password
            else:
                print(f"No split_hashed_password found for username: {username}\n")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return None
    

    def get_salt(self, username: str):
        try:
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT salt FROM PasswordData WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchone()

            if result:
                salt = result[0]
                print(f"salt  for {username}: {salt}\n")
                return salt
            else:
                print(f"No salt found for username: {username}\n")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return None
    

    def get_hashing_data(self, username: str):
        try:
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                SELECT algorithm, version, memorycost, timecost, parallelism, salt, hash_len, salt_len, split_hashed_password 
                FROM PasswordData WHERE username = ?
            ''', (username,))
                
            result = self.cursor.fetchone()

            if result:
                algorithm, version, memory_cost, time_cost, parallelism, salt, hash_len, salt_len, master_password = result
                # !! delete these prints after completion of class (security breach)
                print(f"Data for {username}:")
                print(f"Algorithm: {algorithm}")
                print(f"Version: {version}")
                print(f"Memory Cost: {memory_cost}")
                print(f"Time Cost: {time_cost}")
                print(f"Parallelism: {parallelism}")
                print(f"Salt: {salt}")
                print(f"hash_len: {hash_len}")
                print(f"hash_len: {salt_len}")
                print(f"Master Password: {master_password}\n")

                return {
                    'algorithm': algorithm,
                    'version': version,
                    'memory_cost': memory_cost,
                    'time_cost': time_cost,
                    'parallelism': parallelism,
                    'salt': salt,
                    'hash_len': hash_len,
                    'salt_len': salt_len,
                    'master_password': master_password
                }
            else:
                print(f"No data found for username: {username}\n")
                return None
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#   UserData database
#//////////////////////////////////////////////////////////////////////////////////////////////////////////

# TODO: ChestController (affiche les password avec les services)
#   get the following data :
# service_name 
# password 
    def get_all_user_service_password(self, username: str):
        try:
            #   Prepared statement to get the user's details
            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            self.cursor.execute('''
                SELECT service_name, password FROM UserData WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchall()
            if not result:
                print(f"\nUser {username} not found.\n")
                return None

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return result
    

    def get_user_service_password(self, username: str, service: str):
        try:
            #   Prepared statement to get the user's details
            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            self.cursor.execute('''
                SELECT service_name, password FROM UserData WHERE username = ? AND service_name = ?
            ''', (username, service))
            
            result = self.cursor.fetchall()  # Fetch the result (None if no result) 
            
            if not result:
                print(f"\nUser {username} not found.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return result

    
    def get_all_services(self, username: str):
        try:
            #   Prepared statement to get the user's details
            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            self.cursor.execute('''
                SELECT * FROM UserData WHERE username = ?
            ''', (username,))
            
            result = self.cursor.fetchall()
            
            if not result:
                print(f"\nUser {username} not found.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return result


    def delete_service(self, username: str, service_name: str, password: str):
        try:
            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            self.cursor.execute('''
                DELETE FROM UserData WHERE username = ? AND service_name = ? AND password = ?
            ''', (username, service_name.lstrip(), password.lstrip()))
            self.connection_user.commit()
            return True
        except sqlite3.IntegrityError as e:
            return False

#//////////////////////////////////////////////////////////////////////////////////////////////////////////
#   Setters
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def set_username_folder(self, new_username: str):
        self.username_folder = new_username


    def set_absolute_paths(self):
        self.absolute_path_password = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder, self.db_password_name)
        self.absolute_path_user = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.username_folder, self.db_user_name)


    def create_user(self, user: object):
        try:
            #   Insert into MasterPassword (User) table
            #   and not 'user.hash_password'
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                INSERT INTO User (username, full_hashed_password) 
                VALUES (?, ?)
            ''', (user.get_username(), user.get_full_hash_password()))

            #   Insert into PasswordData (Hashed password splited) table
            self.cursor.execute('''
                INSERT INTO PasswordData (username, algorithm, version, memorycost, timecost, parallelism, salt, hash_len, salt_len, split_hashed_password) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user.get_username(), user.get_param("algorithm"), user.get_param("version"), user.get_param("memory_cost"), user.get_param("time_cost"), user.get_param("parallelism"), user.get_param("salt"), user.get_param("hash_len"), user.get_param("salt_len"), user.get_param("hash_password")))
            
            self.connection_pswd.commit()
            print(f"\nUser {user.username} and master password added to the database.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


    def create_user_passwords(self, username: str, service_name: str, password: str):
        self.get_db_cursor(DEFAULT_DB_USER_NAME)
        self.cursor.execute('''
            INSERT INTO UserData (username, service_name, password) 
            VALUES (?, ?, ?)
        ''', (username, service_name, password))

        self.connection_user.commit()
        print(f"User password for \"{service_name}\" added to the database.")


    def update_master_password(self, user: object, new_hashed_password: str):
        #   Need user input to change the Password data
        new_hash = HashModel.hash_password(new_hashed_password, user)
        HashModel.split_password(user.get_all_params(), new_hash)

        try:
            #   Update the master password
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                UPDATE User SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, user.get_username()))
            
            self.cursor.execute('''
                UPDATE PasswordData SET hashed_password = ? WHERE username = ?
            ''', (new_hashed_password, user.get_username()))
            
            self.connection_pswd.commit()
            print(f"Master password updated for user {user.get_username()}.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


    def delete_user(self, user: object):
        try:
            #   Delete from PasswordData first to maintain referential integrity (since it has a foreing key to username)
            #   Then delete the user
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                DELETE FROM PasswordData WHERE username = ?
            ''', (user.get_username(),))

            self.cursor.execute('''
                DELETE FROM User WHERE username = ?
            ''', (user.get_username(),))
            self.connection_pswd.commit()

            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            #   Then delete the user
            self.cursor.execute('''
                DELETE FROM UserData WHERE username = ?
            ''', (user.get_username(),))
            self.connection_user.commit()

            print(f"User {user.get_username()} deleted from the database.")
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
            return False
