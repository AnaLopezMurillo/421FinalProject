# Users
create_user_table = """CREATE TABLE users (
uid int NOT NULL AUTO_INCREMENT,
name VARCHAR(255) NOT NULL unique,
score int NOT NULL DEFAULT 0,
password VARCHAR(255) NOT NULL,
PRIMARY KEY (uid)
)
"""

create_user_procedure = """CREATE PROCEDURE create_user(IN name TEXT, IN password TEXT)
BEGIN
    INSERT INTO users (name, password) VALUES (name, password);
END
"""

# Posts 
create_post_table = """CREATE TABLE posts (
pid int NOT NULL AUTO_INCREMENT,
word text NOT NULL,
definition text NOT NULL,
upvotes int DEFAULT 0,
downvotes int DEFAULT 0,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
uid int NOT NULL,
PRIMARY KEY (pid),
FOREIGN KEY (uid)
    REFERENCES users(uid)
    ON DELETE CASCADE
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
    ORDER BY created DESC;
END
"""


# Relationship table for interactions
create_interactions_table = """CREATE TABLE interactions (
uid int NOT NULL,
pid int NOT NULL,
action bit NOT NULL,
FOREIGN KEY (uid) 
    REFERENCES users(uid)
    ON DELETE CASCADE,
FOREIGN KEY (pid)
    REFERENCES posts(pid)
    ON DELETE CASCADE
)"""

# Trigger for new interactions
new_interaction_trigger = """CREATE TRIGGER after_interaction_insert 
AFTER INSERT ON interactions
FOR EACH ROW
BEGIN
    -- If action is 1 (upvote)
    IF NEW.action = 1 THEN
        -- Increase score of the post creator
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score + 1
        WHERE p.pid = NEW.pid;
    -- If action is 0 (downvote)
    ELSE
        -- Decrease score of the post creator
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score - 1
        WHERE p.pid = NEW.pid;
    END IF;
END
"""

# Trigger for updating interactions

update_interaction_trigger = """CREATE TRIGGER after_interaction_update 
AFTER UPDATE ON interactions
FOR EACH ROW
BEGIN
    -- If action changed from downvote to upvote
    IF OLD.action = 0 AND NEW.action = 1 THEN
        -- Increase score by 2 (remove downvote and add upvote)
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score + 2
        WHERE p.pid = NEW.pid;
    -- If action changed from upvote to downvote
    ELSEIF OLD.action = 1 AND NEW.action = 0 THEN
        -- Decrease score by 2 (remove upvote and add downvote)
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score - 2
        WHERE p.pid = NEW.pid;
    END IF;
END"""

# Trigger for deleting interactions
delete_interaction_trigger = """CREATE TRIGGER after_interaction_delete 
AFTER DELETE ON interactions
FOR EACH ROW
BEGIN
    -- If deleted action was an upvote
    IF OLD.action = 1 THEN
        -- Decrease score (remove upvote)
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score - 1
        WHERE p.pid = OLD.pid;
    -- If deleted action was a downvote
    ELSE
        -- Increase score (remove downvote)
        UPDATE users u
        JOIN posts p ON p.uid = u.uid
        SET u.score = u.score + 1
        WHERE p.pid = OLD.pid;
    END IF;
END"""
