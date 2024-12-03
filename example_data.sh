CONTAINER_TAG="latest"
CONTAINER_NAME="db"
USER_NAME="root"
PASSWORD="twentyone"
TARGET_DIR="db"

mysql-exec() {
    docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "USE mydatabase; $1" --connect-expired-password
}

# Users
mysql-exec "
INSERT INTO users (name, score, password) VALUES
('john_doe', 15, 'hashed_password_1'),
('jane_smith', 8, 'hashed_password_2'),
('word_wizard', 25, 'hashed_password_3'),
('dictionary_king', -2, 'hashed_password_4'),
('language_lover', 12, 'hashed_password_5');"

mysql-exec "
INSERT INTO users (name, score, password) VALUES
('vocab_master', 30, 'hashed_password_6'),
('word_smith', -5, 'hashed_password_7'),
('lexicon_pro', 18, 'hashed_password_8'),
('grammar_guru', 22, 'hashed_password_9'),
('syntax_sage', 14, 'hashed_password_10'),
('etymology_expert', 9, 'hashed_password_11'),
('phrase_finder', 11, 'hashed_password_12'),
('word_wanderer', 7, 'hashed_password_13'),
('definition_dude', -3, 'hashed_password_14'),
('language_lady', 16, 'hashed_password_15');"


# Posts Table:
mysql-exec "
INSERT INTO posts (word, definition, upvotes, downvotes, uid) VALUES
('ephemeral', 'Lasting for a very short time', 5, 1, 1),
('serendipity', 'The occurrence of finding pleasant things by chance', 8, 2, 2),
('ubiquitous', 'Present, appearing, or found everywhere', 12, 3, 3),
('pellucid', 'Transparently clear in style or meaning', 3, 5, 4),
('mellifluous', 'Sweet or musical; pleasant to hear', 6, 1, 5),
('ethereal', 'Extremely delicate and light', 4, 0, 1),
('perspicacious', 'Having a ready insight into things', 7, 2, 2),
('ineffable', 'Too great to be expressed in words', 9, 1, 3),
('euphoria', 'A feeling of intense excitement and happiness', 5, 3, 4),
('surreptitious', 'Kept secret, especially because improper', 4, 2, 5);
"

mysql-exec "
INSERT INTO posts (word, definition, upvotes, downvotes, uid) VALUES
('laconic', 'Using few words; concise and pithy', 7, 2, 6),
('zeitgeist', 'The defining spirit or mood of a particular period', 10, 1, 7),
('paradigm', 'A typical example or pattern of something', 6, 3, 8),
('mercurial', 'Subject to sudden or unpredictable changes of mood', 8, 2, 9),
('eloquent', 'Fluent or persuasive in speaking or writing', 12, 1, 10),
('esoteric', 'Intended for or understood by only a small number of people', 5, 4, 11),
('verbose', 'Using more words than needed; wordiness', 4, 6, 12),
('quintessential', 'Representing the most perfect example of a quality', 9, 1, 13),
('pontificate', 'Express one\'s opinions in a pompous way', 3, 7, 14),
('nebulous', 'Unclear, vague, or ill-defined', 8, 2, 15),
('prescient', 'Having knowledge of events before they take place', 11, 1, 6),
('sagacious', 'Having good judgment and keen mental discernment', 7, 3, 7),
('perfidious', 'Deceitful and untrustworthy', 5, 2, 8),
('ephemeral', 'Lasting for a very short time', 9, 1, 9),
('sycophant', 'A person who acts obsequiously toward someone to gain advantage', 6, 4, 10);"

# Interactions Table:
mysql-exec "
INSERT INTO interactions (uid, pid, action) VALUES
(1, 2, 1),  -- User 1 upvoted post 2
(1, 3, 1),  -- User 1 upvoted post 3
(2, 1, 1),  -- User 2 upvoted post 1
(2, 4, 0),  -- User 2 downvoted post 4
(3, 5, 1),  -- User 3 upvoted post 5
(3, 6, 1),  -- User 3 upvoted post 6
(4, 7, 0),  -- User 4 downvoted post 7
(4, 8, 1),  -- User 4 upvoted post 8
(5, 9, 1),  -- User 5 upvoted post 9
(5, 10, 0); -- User 5 downvoted post 10
"

mysql-exec "INSERT INTO interactions (uid, pid, action) VALUES
(6, 11, 1),  -- User 6 upvoted post 11
(6, 12, 1),  -- User 6 upvoted post 12
(7, 13, 0),  -- User 7 downvoted post 13
(7, 14, 1),  -- User 7 upvoted post 14
(8, 15, 1),  -- User 8 upvoted post 15
(8, 16, 0),  -- User 8 downvoted post 16
(9, 17, 1),  -- User 9 upvoted post 17
(9, 18, 1),  -- User 9 upvoted post 18
(10, 19, 0), -- User 10 downvoted post 19
(10, 20, 1), -- User 10 upvoted post 20
(11, 21, 1), -- User 11 upvoted post 21
(12, 22, 0), -- User 12 downvoted post 22
(13, 23, 1), -- User 13 upvoted post 23
(14, 24, 1), -- User 14 upvoted post 24
(15, 25, 0), -- User 15 downvoted post 25
(6, 15, 1),  -- User 6 upvoted post 15
(7, 16, 0),  -- User 7 downvoted post 16
(8, 17, 1),  -- User 8 upvoted post 17
(9, 18, 1),  -- User 9 upvoted post 18
(10, 19, 0); -- User 10 downvoted post 19
"