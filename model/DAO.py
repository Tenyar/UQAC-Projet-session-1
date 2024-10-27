# https://docs.python.org/3/library/sqlite3.html (lien vers la doc sqlite3 pour python)
import sqlite3
import os
import sys

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_DB_USER_NAME, DEFAULT_DB_PASSWORD_NAME
)


class DAO:
    def __init__(self, username):
        #   Prepare the second DB for passwords
        self.db_password_name = DEFAULT_DB_PASSWORD_NAME
        #   Arbitrary name (until user can write a name for it)
        self.db_user_name = DEFAULT_DB_USER_NAME
        #   Variable that stores the database in the name of the user
        self.folder_username = None
        #   Path for checking if the file(DB) exist inside the app
        #   Adding names of user to keep a database for a specific user
        self.username_folder = username
        self.absolute_path_password = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', username, self.db_password_name)
        self.absolute_path_user = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', username, self.db_user_name)
            
        #self.connection = None
        self.cursor = None
    

    def connect(self, db_type):
        #   Create the database in the "database/" folder
        #   Connect to the SQLite database. If it doesn't exist, it will be created.
        if not os.path.exists(self.absolute_path_password) and not os.path.exists(self.absolute_path_user):
            print("\nabsolute path for password db : ", self.absolute_path_password)
            print("\nabsolute path for user db : ", self.absolute_path_user)
            while(self.db_user_name == self.db_password_name):
                self.db_user_name = input("[ERROR] : the user DB can't have the same name as the 'password.db', please retry : \n")

            # Create the folder for DB if it don't
            folder_path = os.path.dirname(self.absolute_path_user)
            print("FLLL : ", folder_path)
            if not os.path.exists(folder_path):
                print(f"Creating directory for user database at: {folder_path}")
                os.makedirs(folder_path)  # Create the folder of the username

            #   Formatting the name to be suited for creating a DB
            self.db_user_name = self.db_user_name + ".db"
            print(f"Database not found. Creating a new one at {"database", self.db_user_name}.")

            #   Create both databases
            self.connection_pswd = sqlite3.connect(self.absolute_path_password)
            self.connection_user = sqlite3.connect(self.absolute_path_user)

            self.create_passwords_tables()
            self.create_user_tables()
        else:
            #   Connect both databases
            self.connection_pswd = sqlite3.connect(self.absolute_path_password)
            self.connection_user = sqlite3.connect(self.absolute_path_user)
            #   Either connect to the user database or the password database
            if(db_type == DEFAULT_DB_USER_NAME):
                print(f"Connecting to the existing database at {self.db_user_name}.")
                self.connection_user = sqlite3.connect(self.absolute_path_user)
                self.cursor = self.connection_user.cursor()
            elif (db_type == DEFAULT_DB_PASSWORD_NAME):
                print(f"Connecting to the existing database at {self.db_password_name}.")
                self.connection_pswd = sqlite3.connect(self.absolute_path_password)
                self.cursor = self.connection_pswd.cursor()


    def close(self):
        #Close the database connection.
        #if self.connection:
        #    self.connection.close()

        if self.connection_pswd:
            self.connection_pswd.close()

        if self.connection_user:
            self.connection_user.close()


    #   Method to get the cursor for one of the connection to one of the 2 databases for a user.
    # Cursor = Variable switching between user and password db to provide a way to use sql query.
    def get_db_cursor(self, db_type):
        if(db_type == DEFAULT_DB_PASSWORD_NAME):
            self.cursor = self.connection_pswd.cursor()
        elif(db_type == DEFAULT_DB_USER_NAME):
            self.cursor = self.connection_user.cursor()


    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
    #   Creating the databases
    #//////////////////////////////////////////////////////////////////////////////////////////////////////////
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
            
        # !!! Est-ce utile ou de la redondance
#       cursor.execute('''
#           CREATE TABLE IF NOT EXISTS User (
#               username TEXT PRIMARY KEY,
#           )
#       ''')
        self.get_db_cursor(DEFAULT_DB_USER_NAME)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserData (
                username TEXT NOT NULL,
                site_or_app_name TEXT NOT NULL,
                password TEXT NOT NULL
            ) 
        ''')    # FOREIGN KEY(username) REFERENCES User(username)
        self.connection_user.commit()

    #   CRUD methods for databases
    # connection_type = connected to user or password table ?
    def create_user(self, user):
        #   Gestion d'erreur sur la contrainte unique d'un utilisateur
        while self.get_user_by_username(user.username):
            print(f"[ERROR] : the username {user.username} is arleady taken, please retry : ")
            new_username = input()
            user.set_username(new_username)

        try:
            # Insert into MasterPassword (User) table
            # and not 'user.hash_password'
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                INSERT INTO User (username, full_hashed_password) 
                VALUES (?, ?)
            ''', (user.username, user.full_hash_value))

            # Insert into PasswordData (Hashed password splited) table
            self.cursor.execute('''
                INSERT INTO PasswordData (username, algorithm, version, memorycost, timecost, parallelism, salt, hash_len, salt_len, split_hashed_password) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user.username, user.hash_params["algorithm"], user.hash_params["version"], user.hash_params["memory_cost"], user.hash_params["time_cost"], user.hash_params["parallelism"], user.hash_params["salt"], user.hash_params["hash_len"], user.hash_params["salt_len"], user.hash_params["hash_password"]))
            
            self.connection_pswd.commit()
            print(f"User {user.username} and master password added to the database.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


    #   Prepared request for safety (for sql)
    def get_user_by_username(self, username):
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


    def get_fullhashed_master_password(self, username):
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

        return None


    def get_hashed_master_password(self, username):
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
    
    
    def get_salt(self, username):
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
    

    def get_hashing_data(self, username):
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

        return None


    def update_master_password(self, user, new_hashed_password):
        try:
            # Update the master password
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                UPDATE User SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, user.username))
            
            self.cursor.execute('''
                UPDATE PasswordData SET hashed_password = ? WHERE username = ?
            ''', (new_hashed_password, user.username))
            
            self.connection_pswd.commit()
            print(f"Master password updated for user {user.username}.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")


    def delete_user(self, user):
        try:
            # Delete from PasswordData first to maintain referential integrity (since it has a foreing key to username)
            # Then delete the user
            self.get_db_cursor(DEFAULT_DB_PASSWORD_NAME)
            self.cursor.execute('''
                DELETE FROM PasswordData WHERE username = ?
            ''', (user.username,))

            self.cursor.execute('''
                DELETE FROM User WHERE username = ?
            ''', (user.username,))
            self.connection_pswd.commit()

            self.get_db_cursor(DEFAULT_DB_USER_NAME)
            # Then delete the user
            self.cursor.execute('''
                DELETE FROM UserData WHERE username = ?
            ''', (user.username,))
            self.connection_user.commit()

            print(f"User {user.username} deleted from the database.")
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")






#  def __init__(self, db_connection):
#      self.connection = db_connection
#      #   execute SQL statements and fetch results from SQL queries
#      self.cur = db_connection.cursor()
#
#  #   CRUD methods for databases
#  def create(self, data):
#      
#  #   Prepared request for safety (for sql)
#  def read(self, data):
#
#  def update(self, data):
#
#  def delete(self, data):
#  
#  #con = sqlite3.connect("PasswordManager.db")