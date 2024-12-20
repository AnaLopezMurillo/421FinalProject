import PySimpleGUI as sg
import db
from post import Post

db.init()

# vars
username = ''
password = ''
uid = ''


def login():
    return [
        [sg.Text("Login Page", font='Bold', justification='center', expand_x=True)],
        [sg.Text('Username', font='Bold', justification='center', expand_x=True), sg.InputText(key='-USERNAME-')],
        [sg.Text('Password', font='Bold', justification='center', expand_x=True), sg.InputText(password_char='*', key='-PASSWORD-')],
        [sg.Text("", expand_x=True), sg.Button("Login", font='bold')]
    ]

def home(posts):
    if not posts:
        post_elements = [[sg.Text("No posts available.", justification='center', expand_x=True)]]
    else:
        post_elements = []
        for i, post in enumerate(posts[:10]):  # Limit to 10 posts
            if i % 3 == 0:
                post_elements.append([])  # Start a new row every 3 posts
            post_elements[-1].append(
                sg.Frame(
                    layout=[
                        [sg.Text(f"Term: {post.word}", font='bold')],
                        [sg.Text(f"Definition: {post.definition}")],
                        [sg.Text(f"Upvotes: {post.upvotes}", text_color='#32CD32'), sg.Text(f"Downvotes: {post.downvotes}", text_color='red')],
                        [sg.Button("Upvote", key=f"UPVOTE_{i}"), sg.Button("Downvote", key=f"DOWNVOTE_{i}")]
                    ],
                    title="Post",
                    relief=sg.RELIEF_SUNKEN,
                    pad=(5, 5),
                    border_width=2
                )
            )

    return [
        [sg.Button("Sign Out", font='bold'), sg.Text("", key='-USERNAME-DISPLAY-', font='bold', justification='center', expand_x=True), sg.Button("Profile", font='bold')],
        [sg.Text("Recent Posts", font='bold',justification='center'), sg.Text("", expand_x=True), sg.Button("Add Record", font='bold')],
        [sg.Column(post_elements, scrollable=True, vertical_scroll_only=True, size=(480, 300))]
    ]

def profile(posts):
    if not posts:
        post_elements = [[sg.Text("No posts available.", justification='center', expand_x=True)]]
    else:
        post_elements = []
        for i, post in enumerate(posts[:10]):  # Limit to 10 posts
            if i % 2 == 0:
                post_elements.append([])  # Start a new row every 2 posts
            post_elements[-1].append(
                sg.Frame(
                    layout=[
                        [sg.Text(f"Term: {post.word}", font='bold')],
                        [sg.Text(f"Definition: {post.definition}")],
                        [sg.Text(f"Upvotes: {post.upvotes}", text_color='#32CD32'), sg.Text(f"Downvotes: {post.downvotes}", text_color='red')],
                        [sg.Button("Delete", key=f"DELETE_{i}")]
                    ],
                    title="Post",
                    relief=sg.RELIEF_SUNKEN,
                    pad=(5, 5),
                    border_width=2
                )
            )

    return [
        [sg.Button("Home", font='bold'), sg.Text("Profile", font='bold', justification='center', expand_x=True)],
        [sg.Text("Your Posts", font='bold', justification='center', expand_x=True)],
        [sg.Column(post_elements, scrollable=True, vertical_scroll_only=True, size=(300, 250))]
        
    ]

def add_record():
    return [
        [sg.Button("Home", font='bold'), sg.Text("Add Record", font='bold', justification='center', expand_x=True), sg.Button("Profile", font='bold')],
        [sg.Text("Term", justification='center', expand_x=True), sg.InputText(key='-TERM-')],
        [sg.Text("Definition",justification='center', expand_x=True), sg.InputText(key='-DEF-')],
        [sg.Text("", key='-ADDRECORD-DISPLAY-'), sg.Text("", expand_x=True), sg.Button("Submit", font='bold')],
    ]

# Set the initial window with the main layout
window = sg.Window("Router Example", login(), finalize=True, size=(300,150))
window['-PASSWORD-'].bind("<Return>", "Login")

# Initialize posts
posts = db.get_posts(0)

# Event loop for routing
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event.startswith("UPVOTE_"):
        index = int(event.split("_")[1])
        posts = db.get_posts()  # Refresh posts
        post = posts[index]
        if not db.upvote_post(uid, post.pid):
            sg.popup("You have already upvoted this post.")
        posts = db.get_posts()  # Refresh posts
        window.close()
        window = sg.Window("Home", home(posts), finalize=True, size=(530, 270))
    elif event.startswith("DOWNVOTE_"):
        index = int(event.split("_")[1])
        posts = db.get_posts()  # Refresh posts
        post = posts[index]
        if not db.downvote_post(uid, post.pid):
            sg.popup("You have already downvoted this post.")
        posts = db.get_posts()  # Refresh posts
        window.close()
        window = sg.Window("Home", home(posts), finalize=True, size=(530, 270))
    elif event.startswith("DELETE_"):
        index = int(event.split("_")[1])
        user_posts = db.get_posts_by_user(uid)  # Refresh user posts
        if index < len(user_posts):
            post = user_posts[index]
            db.delete_post(post.pid)
            user_posts = db.get_posts_by_user(uid)  # Refresh user posts again after deletion
            window.close()
            window = sg.Window("Profile", profile(user_posts), finalize=True, size=(350, 250))
        else:
            sg.popup("Error: Post not found.")
    elif event == "Login" or event == ("-PASSWORD-" + "Login"):
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        if db.login_user(username, password):
            uid = db.get_user(username)[0]
            window.close()
            window = sg.Window("Home", home(posts), finalize=True, size=(530, 270))
            # this changes the title of the window to the user's name
            # probably also how we will want to update user info through GET calls
            window['-USERNAME-DISPLAY-'].update(username + "'s Home") 
        else:
            if db.create_user(username, 0, password):
                uid = db.get_user(username)[0]
                window.close()
                window = sg.Window("Home", home(posts), finalize=True)
                window['-USERNAME-DISPLAY-'].update(username + "'s Home") 
                sg.popup("You didn't have a profile, so we made one for you! I hope you remember that password...")
            else:
                sg.popup("Error: This username is already taken.")

    elif event == "Profile":
        user_posts = db.get_posts_by_user(uid)  # Use uid instead of username
        window.close()
        window = sg.Window("Profile", profile(user_posts), finalize=True, size=(350, 250))
    elif event == "Sign Out":
        window.close()
        window = sg.Window("Login", login(), finalize=True, size=(300,150))
        window['-PASSWORD-'].bind("<Return>", "Login")
    elif event == "Home":
        window.close()
        window = sg.Window("Home", home(db.get_posts()), finalize=True, size=(530, 270))
        window['-USERNAME-DISPLAY-'].update(username + "'s Home")
    elif event == "Add Record":
        window.close()
        window = sg.Window("Record", add_record(), finalize=True)
        
    elif event == "Submit":
        term = values['-TERM-']
        definition = values['-DEF-']
        if term and definition:
            try:
                db.create_post(term, definition, uid)

                # Update the UI with a success message
                sg.popup(f"Term '{term}' added successfully!")
                window['-DEF-'].update("")
                window['-TERM-'].update("")
                window['-ADDRECORD-DISPLAY-'].update(f"Term '{term}' added!")
            except Exception as e:
                sg.popup(f"Error adding term: {e}")
        else:
            sg.popup("Please fill in both Term and Definition fields.")

    # name = values[0]
    # password = values[1]
    
window.close()
db.close_cursor()