# Users table
# create_user_table = """CREATE TABLE users (
# uid int NOT NULL,
# name text NOT NULL,
# score int,
# password text make secure later
# PRIMARY KEY (uid)
# )
# """

create_user_table = """CREATE TABLE users (
uid int NOT NULL AUTO_INCREMENT,
name text NOT NULL,
score int NOT NULL DEFAULT 0,
password text NOT NULL,
PRIMARY KEY (uid)
)
"""

create_user_procedure = """CREATE PROCEDURE create_user(IN name TEXT, IN password TEXT)
BEGIN
    INSERT INTO users (name, password) VALUES (name, password);
END
"""


# Posts table
create_post_table = """CREATE TABLE posts (
pid int NOT NULL AUTO_INCREMENT,
word text NOT NULL,
definition text NOT NULL,
upvotes int DEFAULT 0,
downvotes int DEFAULT 0,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
uid int NOT NULL,
PRIMARY KEY (pid),
FOREIGN KEY (uid) REFERENCES users(uid)
)"""

create_post_procedure = """CREATE PROCEDURE create_post(IN word TEXT, IN definition TEXT, IN uid INT)
BEGIN
    INSERT INTO posts (word, definition, uid) VALUES (word, definition, uid);
END
"""

get_posts_page_procedure = """CREATE PROCEDURE get_posts_by_page(IN page INT) 
BEGIN
    
    DECLARE offset_value INT;
    
    SET offset_value = page * 10;  -- Calculate the offset

    SELECT * FROM posts 
    ORDER BY created DESC
    LIMIT 10 OFFSET offset_value;
END
"""

get_posts_user_procedure = """CREATE PROCEDURE get_posts_by_user(IN uid INT) 
BEGIN
    SELECT * FROM posts P 
    WHERE P.uid = uid
    ORDER BY created DESC;e
END
"""


# Relationship table for interactions
create_interactions_table = """CREATE TABLE interactions (
uid int NOT NULL,
pid int NOT NULL,
action bit NOT NULL,
FOREIGN KEY (uid) REFERENCES users(uid),
FOREIGN KEY (pid) REFERENCES posts(pid)
)"""