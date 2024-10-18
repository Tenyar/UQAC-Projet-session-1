# https://docs.python.org/3/library/sqlite3.html (lien vers la doc sqlite3 pour python)
import sqlite3
import os


class DAO:
    def __init__(self, db_path='password_manager.db'):
        self.db_path = db_path
        self.connection = None
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
                master_password TEXT NOT NULL,
                timecost INTEGER NOT NULL,
                memorycost INTEGER NOT NULL,
                parallelism INTEGER NOT NULL,
                hash_len INTEGER NOT NULL,
                salt_len INTEGER NOT NULL,
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

    def create_user(conn, username, hashed_password, timecost, memorycost, parallelism, hash_len, salt_len):
        cursor = conn.cursor()
        
        try:
            # Insert into User table
            cursor.execute('''
                INSERT INTO User (username, master_password) 
                VALUES (?, ?)
            ''', (username, hashed_password))
            
            # Insert into MasterPassword table
            cursor.execute('''
                INSERT INTO MasterPassword (username, master_password, timecost, memorycost, parallelism, hash_len, salt_len) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, timecost, memorycost, parallelism, hash_len, salt_len))
            
            conn.commit()
            print(f"User {username} and master password added to the database.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
            
    #   Prepared request for safety (for sql)
    def get_user(conn, username):
        cursor = conn.cursor()
        
        try:
            # Prepared statement to get the user's details
            cursor.execute('''
                SELECT * FROM User WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            
            if user:
                print(f"User found: {user}")
            else:
                print(f"User {username} not found.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

        return user
            
    def update_master_password(conn, username, new_hashed_password):
        cursor = conn.cursor()
        
        try:
            # Update the master password
            cursor.execute('''
                UPDATE User SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, username))
            
            cursor.execute('''
                UPDATE MasterPassword SET master_password = ? WHERE username = ?
            ''', (new_hashed_password, username))
            
            conn.commit()
            print(f"Master password updated for user {username}.")

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")

    def delete_user(conn, username):
        cursor = conn.cursor()
        try:
            # Delete from MasterPassword first to maintain referential integrity (since it has a foreing key to username)
            cursor.execute('''
                DELETE FROM MasterPassword WHERE username = ?
            ''', (username,))
            
            # Then delete the user
            cursor.execute('''
                DELETE FROM User WHERE username = ?
            ''', (username,))
            
            conn.commit()
            print(f"User {username} deleted from the database.")
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