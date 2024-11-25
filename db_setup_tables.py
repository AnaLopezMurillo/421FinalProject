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
uid int NOT NULL,
name text NOT NULL,
score int,
password text,
PRIMARY KEY (uid)
)
"""

# Posts table
create_post_table = """CREATE TABLE posts (
pid int NOT NULL,
word text NOT NULL,
definition text NOT NULL,
upvotes int,
downvotes int,
uid int,
PRIMARY KEY (pid),
FOREIGN KEY (uid) REFERENCES users(uid)
)"""

# Relationship table for interactions
create_interactions_table = """CREATE TABLE interactions (
uid int NOT NULL,
pid int NOT NULL,
action bit NOT NULL,
FOREIGN KEY (uid) REFERENCES users(uid),
FOREIGN KEY (pid) REFERENCES posts(pid)
)"""