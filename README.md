# 421FinalProject

### User interface: 
PySimpleGUI
https://docs.pysimplegui.com/en/latest/

### Backend:
Docker with MySQL instance

### Database:


Posts: One to many relationship w/ users
- Id
- Word
- Definition
- User it links to 
- no. upvotes
- no. downvotes
- score, but when a user likes a post this is a transaction so every upvote/downvote accounted for

User:
- Id
- Name
- Password (keep secure)

Relationship table (interactions):
- Keep track of id's where user has interacted with post

Logging in/trigger:
- Search for username check, if not present then make a new account else say account exists 

Data Validation:
- Password strength/secure password? Certain length/certain characters, etc.

Secure Password Storage:
- Hash? Plain text

Procedure:
- Function for the database - query you would make and making it a function