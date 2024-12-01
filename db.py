"""This module contains functions for interacting with the database."""
import mysql.connector
import db_setup_tables
import hashlib


# DB connection info
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "twentyone"
DB_NAME = "mydatabase"

# DB connection and cursor
mydb: mysql.connector.connection.MySQLConnection = None
cursor: mysql.connector.cursor.MySQLCursor = None


def init(): 
    """Initializes the database connection and cursor."""
    global mydb, cursor
    mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = mydb.cursor()
    cursor.execute(f"USE {DB_NAME}")

def get_cursor():
    """Returns the cursor."""
    return cursor
  
def close_cursor():
    """Closes the cursor."""
    cursor.close()
  
def create_user(name: str, score: int, password: str):
    """Creates a user in the database."""
    cursor.execute(f"INSERT INTO users (name, score, password) VALUES ('{name}', {score}, '{password}')")
    
def create_post(word: str, definition: str, uid: int):
    """Creates a post in the database."""
    cursor.execute("CALL create_post(%s, %s, %s)", (word, definition, uid))
    # cursor.execute(f"INSERT INTO posts (word, definition, upvotes, downvotes, uid) VALUES ('{word}', '{definition}', {upvotes}, {downvotes}, {uid})")
    
def create_interaction(uid: int, pid: int, action: bool):
    """Creates an interaction in the database."""
    cursor.execute(f"INSERT INTO interactions (uid, pid, action) VALUES ({uid}, {pid}, {action})")

def login_user(name: str, password: str):
    """Logs in a user."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    print(f"Hashed password: {hashed_password}")
    query = f"SELECT name FROM users WHERE name = '{name}' AND password = '{hashed_password}'"
    cursor.execute(query)
    output = cursor.fetchall()
    if len(output) == 0:
        return False
    print(output)
    if output[0][0] == name:
        return True
    return False

if __name__ == "__main__":
    # Initializes the database and creates the tables.
    init_db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

    init_cursor = init_db.cursor()

    init_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    init_cursor.execute(f"USE {DB_NAME}")
    try:
        init_cursor.execute(db_setup_tables.create_user_table)
        print("Users table created successfully.")
    except mysql.connector.errors.ProgrammingError:
        print("Users table already exists")
    try:
        init_cursor.execute(db_setup_tables.create_post_table)
        print("Posts table created successfully.")
    except mysql.connector.errors.ProgrammingError:
        print("Posts table already exists")
    try:
        init_cursor.execute(db_setup_tables.create_interactions_table)
        print("Interactions table created successfully.")
    except mysql.connector.errors.ProgrammingError:
        print("Interactions table already exists")
    print("Tables created successfully.")
    
    
    try:
        init_cursor.execute(db_setup_tables.create_user_procedure)
        print("User procedure created successfully.")
    except mysql.connector.errors.ProgrammingError:
        print("User procedure already exists")
    
    try:
        init_cursor.execute(db_setup_tables.create_post_procedure)
        print("Post procedure created successfully.")
    except mysql.connector.errors.ProgrammingError:
        print("Post procedure already exists")
        
    print("Procedures created successfully.")
    
    try:
        init_cursor.execute("INSERT INTO users (name, password) VALUES ('test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')")
        print("Test user created successfully.")
    except mysql.connector.errors.IntegrityError:
        print("Test user already exists")
        
    init_db.commit()

    print("\nDatabases:")
    init_cursor.execute("SHOW DATABASES")
    for x in init_cursor:
        print(x)

    print("\nTables:")
    init_cursor.execute("SHOW TABLES")
    for x in init_cursor:
        print(x)

    init_cursor.close()
