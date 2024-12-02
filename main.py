import PySimpleGUI as sg
import db

db.init()
cursor = db.get_cursor()

# vars
username = ''
password = ''

def login():
    return [
        [sg.Text("Login Page", font='Bold', justification='center', expand_x=True)],
        [sg.Text('Username', justification='center', expand_x=True), sg.InputText(key='-USERNAME-')],
        [sg.Text('Password', justification='center', expand_x=True), sg.InputText(password_char='*', key='-PASSWORD-')],
        [sg.Button("Exit"), sg.Text("", expand_x=True), sg.Button("Login")]
    ]

def home():
    return [
        [sg.Button("Back to Login"), sg.Text("", key='-USERNAME-DISPLAY-', font='bold', justification='center', expand_x=True), sg.Button("Profile"),],
        [sg.Text("Posts will go here"),sg.Button("Add Record"),],
        [sg.Button("Exit")]
    ]

def profile(posts):
    post_elements = [[sg.Text(f"{post.word}: {post.definition} (Upvotes: {post.upvotes}, Downvotes: {post.downvotes})")] for post in posts]
    return [
        [sg.Button("Home"), sg.Text("Profile", font='bold', justification='center', expand_x=True)],
        [sg.Text("Profile info + scores will go here")],
        *post_elements,
        [sg.Button("Exit")]
    ]

def add_record():
    return [
        [sg.Button("Home"), sg.Text("Add Record", font='bold', justification='center', expand_x=True), sg.Button("Profile")],
        [sg.Text("Term", justification='center', expand_x=True), sg.InputText(key='-TERM-')],
        [sg.Text("Definition",justification='center', expand_x=True), sg.InputText(key='-DEF-')],
        [sg.Text("", key='-ADDRECORD-DISPLAY-'), sg.Text("", expand_x=True), sg.Button("Submit")],
        [sg.Button("Exit")]
    ]

# Set the initial window with the main layout
window = sg.Window("Router Example", login(), finalize=True)
window['-PASSWORD-'].bind("<Return>", "Login")

# Event loop for routing
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Login" or event == ("-PASSWORD-" + "Login"):
        # grab user and password
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        if db.login_user(username, password):
            window.close()
            window = sg.Window("Home", home(), finalize=True)
            # this changes the title of the window to the user's name
            # probably also how we will want to update user info through GET calls
            window['-USERNAME-DISPLAY-'].update(username + "'s Home") 
        else:
            # User not yet initialized
            db.create_user(username, 0, password)
            window.close()
            window = sg.Window("Home", home(), finalize=True)
            window['-USERNAME-DISPLAY-'].update(username + "'s Home") 

    elif event == "Profile":
        window.close()
        window = sg.Window("Profile", profile(db.get_posts(username)))
    elif event == "Back to Login":
        window.close()
        window = sg.Window("Login", login())
    elif event == "Home":
        window.close()
        window = sg.Window("Home", home(), finalize=True)
        window['-USERNAME-DISPLAY-'].update(username + "'s Home")
    elif event == "Add Record":
        window.close()
        window = sg.Window("Record", add_record(), finalize=True)
    elif event == "Submit":
    # Get the term and definition from the input fields
        term = values['-TERM-']
        definition = values['-DEF-']

        if term and definition:
            try:
                # Use a placeholder user ID (e.g., 1) or retrieve the logged-in user's ID
                user_id = 1
                db.create_post(term, definition, user_id)

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