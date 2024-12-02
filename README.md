# 421FinalProject

### User interface: 
PySimpleGUI
https://docs.pysimplegui.com/en/latest/

### Backend:
Docker with MySQL instance

To setup the database for the first time, run:
```sh
source setup.sh
``` 

You can run the database at anytime after the intial setup with this:
```sh
source db.sh
```
> Note: If you've just run `setup.sh`, and you haven't run `stop.sh` yet, you don't need to run `db.sh` until the next time you want to start the database after properly closing it.

Once you're done with the database, or if you want to close docker or shut down your computer, run the following:
```sh
source stop.sh
```

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
- Overall score (reddit karma)
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

## Pages
- Login
    - and register, little box at bottom if haven't registered
- Posts
    - search bar at top - filters instead of retrieves
    - big plus button on the page with adding a post
    - 
- Profile
    - posts you've interacted 
    - shows your upvotes/downvotes