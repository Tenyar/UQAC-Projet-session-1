# https://docs.python.org/3/library/sqlite3.html (lien vers la doc sqlite3 pour python)
import sqlite3
import os


class DAO:
    def __init__(self, db_path='password_manager.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.absolute_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', self.db_path)

    def connect(self):
        #   Create the database in the "database/" folder
        #   Connect to the SQLite database. If it doesn't exist, it will be created.
        if not os.path.exists(self.absolute_path):
            print(f"Database not found. Creating a new one at {"database", self.db_path}.")
            self.connection = sqlite3.connect(self.absolute_path)
            self.create_tables()
        else:
            print(f"Connecting to the existing database at {self.db_path}.")
            self.connection = sqlite3.connect(self.absolute_path)
            self.cursor = self.connection.cursor()

    def close(self):
        #Close the database connection.
        if self.connection:
            self.connection.close()

    #   CRUD methods for databases
    def create_tables(self):
        #Create the necessary tables if they don't exist.
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                username TEXT PRIMARY KEY,
                master_password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MasterPassword (
                username TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                version TEXT NOT NULL,
                memorycost INTEGER NOT NULL,
                timecost INTEGER NOT NULL,
                parallelism INTEGER NOT NULL,
                salt TEXT NOT NULL,
                master_password TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES User(username)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passwords (
                username TEXT NOT NULL,
                site_app_name TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES User(username)
            )
        ''')
        self.connection.commit()

    def create_user(self, user):
        
        try:
            # Insert into User table
            self.cursor.execute('''
                INSERT INTO User (username, master_password) 
                VALUES (?, ?)
            ''', (user.username, user.hash_password))
            
            # Insert into MasterPassword table
            self.cursor.execute('''
                INSERT INTO MasterPassword (username, master_password, timecost, memorycost, parallelism, hash_len, salt_len) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user.username, user.algorithm, user.version, user.memory_cost, user.time_cost, user.parallelism, user.salt, user.hash_password))
            
            self.connection.commit()
            print(f"User {user.username} and master password added to the database.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
            
    #   Prepared request for safety (for sql)
    def get_user(self, user):
        try:
            # Prepared statement to get the user's details
            self.cursor.execute('''
                SELECT * FROM User WHERE username = ?
            ''', (user.username,))
            
            user = self.cursor.fetchone()
            
            if user:
                print(f"User found: {user}")
            else:
                print(f"User {user.username} not found.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return user
            
    def update_master_password(self, user, new_hashed_password):
        try:
            # Update the master password
            self.cursor.execute('''
                UPDATE User SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, user.username))
            
            self.cursor.execute('''
                UPDATE MasterPassword SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, user.username))
            
            self.conection.commit()
            print(f"Master password updated for user {user.username}.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

    def delete_user(self, user):
        try:
            # Delete from MasterPassword first to maintain referential integrity (since it has a foreing key to username)
            self.cursor.execute('''
                DELETE FROM MasterPassword WHERE username = ?
            ''', (user.username,))
            
            # Then delete the user
            self.cursor.execute('''
                DELETE FROM User WHERE username = ?
            ''', (user.username,))
            
            self.connection.commit()
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
#