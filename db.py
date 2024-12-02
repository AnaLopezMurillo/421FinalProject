"""This module contains functions for interacting with the database."""
import mysql.connector
import db_setup_tables
import hashlib

from post import Post


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
    mydb = mysql.connector.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASSWORD,
        database=DB_NAME
    )
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
    hashed_password = hashlib.sha256(password.encode()).hexdigest()   
    if not login_user(name, password):
        cursor.execute(f"INSERT INTO users (name, score, password) VALUES ('{name}', {score}, '{hashed_password}')")
        print(f"User {name} created successfully.")
        mydb.commit()
      
def create_post(word: str, definition: str, uid: int):
    """Creates a post in the database."""
    try:
        # Use the stored procedure if it exists
        query = "CALL create_post(%s, %s, %s)"
        cursor.execute(query, (word, definition, uid))
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise


def create_interaction(uid: int, pid: int, action: bool) -> int:
    """Creates an interaction in the database. 

    Returns: 0 if no change, -1 if swaps, 1 if a new interaction is created    
        
    """
    # check if the user has already interacted
    # if not, create new interaction
    # if so, check what the interaction was
        # if they had previously downvoted and now are trying to upvote, swap
        # and visa versa
        # otherwise just don't let them do it
    cursor.execute(f"SELECT u.uid, i.action FROM users u INNER JOIN interactions i ON i.uid = u.uid")
    entries = cursor.fetchall()
    if len(entries):
        print("User has already interacted")
        if(entries[0][1] != action):
            # update this entry to match the new action
            print("Swapping action")
            cursor.execute(f"UPDATE interactions i SET i.action = {action} WHERE i.uid = {entries[0][0]}")
            mydb.commit()
            return -1
        else:
            print("User has already done that action")
            return 0
    else:   
        cursor.execute(f"INSERT INTO interactions (uid, pid, action) VALUES ({uid}, {pid}, {action})")
        mydb.commit()
        return 1

def get_posts(page: int = 0):
    """Returns a list of posts."""
    posts = []
    cursor.callproc("get_posts_by_page", [page])
    # Store the results from the first result set
    query_results = cursor.stored_results()
    # Get the first result set
    results = next(query_results).fetchall()
    # print(results)
    for r in results:
        posts.append(Post(word=r[1], pid=r[0], definition=r[2], uid=r[6], upvotes=r[3], downvotes=r[4], created=r[5]))
        # posts.append({
        #     "pid": r[0],
        #     "word": r[1],xw
        #     "definition": r[2],
        #     "upvotes": r[3],
        #     "downvotes": r[4],
        #     "created": r[5],
        #     "uid": r[6]
        # })
    cursor.nextset()
    return posts

def get_posts_by_user(uid: int):
    """Returns a list of posts."""
    posts = []
    cursor.callproc("get_posts_by_user", [uid])
    # Store the results from the first result set
    query_results = cursor.stored_results()
    # Get the first result set
    results = next(query_results).fetchall()
    # print(results)
    for r in results:
        posts.append(Post(word=r[1], pid=r[0], definition=r[2], uid=r[6], upvotes=r[3], downvotes=r[4], created=r[5]))
        # posts.append({
        #     "pid": r[0],
        #     "word": r[1],xw
        #     "definition": r[2],
        #     "upvotes": r[3],
        #     "downvotes": r[4],
        #     "created": r[5],
        #     "uid": r[6]
        # })
    cursor.nextset()
    return posts

def login_user(name: str, password: str):
    """Logs in a user."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # print(f"Hashed password: {hashed_password}")
    query = f"SELECT name FROM users WHERE name = '{name}' AND password = '{hashed_password}'"
    cursor.execute(query)
    output = cursor.fetchall()
    if output is None or len(output) == 0:
        print("User Not Found")
        return False
    # print(output)
    if output[0][0] == name:
        print("User Found: ", output[0])
        return True
    print("User Not Found")
    return False

def get_user(name: str):
    """Returns a user."""
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)
    output = cursor.fetchall()
    if output is None or len(output) == 0:
        print("User Not Found")
        return None
    return output[0]

# def get_posts(username):
#     """Returns all posts from a specific user."""
#     posts = []
#     query = "SELECT p.word, p.definition, u.uid, p.upvotes, p.downvotes FROM posts AS p INNER JOIN users AS u ON p.uid = u.uid WHERE u.name = %s"
#     cursor.execute(query, (username,))
#     entries = cursor.fetchall()
#     for word, definition, uid, upvotes, downvotes in entries:
#         post = Post(word, definition, uid, upvotes, downvotes)
#         print(f"Word: {word}, Definition: {definition}, Upvotes: {upvotes}, Downvotes: {downvotes}")
#         posts.append(post)
#     return posts

# def get_recent_posts(limit=10):
#     """Returns the most recent posts, limited to a specified number."""
#     query = "SELECT pid, word, definition, uid, upvotes, downvotes, created FROM posts ORDER BY pid DESC LIMIT %s"
#     cursor.execute(query, (limit,))
#     entries = cursor.fetchall()
#     posts = [Post(pid, word, definition, uid, upvotes, downvotes, created) for pid, word, definition, uid, upvotes, downvotes in entries]
#     return posts

def upvote_post(uid: int, pid: int):
    """Increases the upvote count for a post."""
    result = create_interaction(uid, pid, True)
    if result == -1:
        # swap upvote to downvote
        query = "UPDATE posts SET upvotes = upvotes + 1, downvotes = downvotes - 1 WHERE pid = %s"
    elif result == 1:
        # add new upvote
        query = "UPDATE posts SET upvotes = upvotes + 1 WHERE pid = %s"
    elif result == 0:
        # no change, they've already upvoted
        return
    cursor.execute(query, (pid,))
    mydb.commit()

def downvote_post(uid: int, pid: int):
    """Increases the downvote count for a post."""
    result = create_interaction(uid, pid, False)
    if result == -1:
        # swap upvote to downvote
        query = "UPDATE posts SET downvotes = downvotes + 1, upvotes = upvotes - 1 WHERE pid = %s"
    elif result == 1:
        # add new upvote
        query = "UPDATE posts SET downvotes = downvotes + 1 WHERE pid = %s"
    elif result == 0:
        # no change, they've already upvoted
        return
    cursor.execute(query, (pid,))
    mydb.commit()

def get_user_id(username: str):
    """Fetches the user ID (uid) for a given username."""
    query = "SELECT uid FROM users WHERE name = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def delete_post(pid: int):
    """Deletes a post from the database."""
    query = "DELETE FROM posts WHERE pid = %s"
    cursor.execute(query, (pid,))
    mydb.commit()

if __name__ == "__main__":
    # Initializes the database and creates the tables.
    init_db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

    init_cursor = init_db.cursor()

    init_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    init_cursor.execute(f"USE {DB_NAME}")
    try:
        init_cursor.execute(db_setup_tables.create_user_table)
        init_cursor.execute(db_setup_tables.create_trigger_name)
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
        init_cursor.execute(db_setup_tables.get_posts_user_procedure)
        init_cursor.execute(db_setup_tables.get_posts_page_procedure)
        print("Post procedures created successfully.")
    except mysql.connector.errors.ProgrammingError as e:
        print("Post procedure already exists")
        print(e)
        
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
