import mysql.connector
import db_setup_tables

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "twentyone"
DB_NAME = "mydatabase"

mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

cursor = mydb.cursor()
cursor.execute(f"USE {DB_NAME}")

def get_cursor():
    return cursor
  
def close_cursor():
    cursor.close()
  
def create_user(name: str, score: int, password: str):
    cursor.execute(f"INSERT INTO users (name, score, password) VALUES ('{name}', {score}, '{password}')")
    
def create_post(word: str, definition: str, upvotes: int, downvotes: int, uid: int):
    cursor.execute(f"INSERT INTO posts (word, definition, upvotes, downvotes, uid) VALUES ('{word}', '{definition}', {upvotes}, {downvotes}, {uid})")
    
def create_interaction(uid: int, pid: int, action: bool):
    cursor.execute(f"INSERT INTO interactions (uid, pid, action) VALUES ({uid}, {pid}, {action})")

if __name__ == "__main__":
    init_cursor = mydb.cursor()

    init_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    init_cursor.execute(f"USE {DB_NAME}")
    init_cursor.execute(db_setup_tables.create_user_table)
    init_cursor.execute(db_setup_tables.create_post_table)
    init_cursor.execute(db_setup_tables.create_interactions_table)
    print("Tables created successfully")

    print("Databases:")
    init_cursor.execute("SHOW DATABASES")
    for x in init_cursor:
        print(x)

    print("Tables:")
    init_cursor.execute("SHOW TABLES")
    for x in init_cursor:
        print(x)

    init_cursor.close()
