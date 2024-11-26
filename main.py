import PySimpleGUI as sg
# import db

# cursor = db.get_cursor()

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

def profile():
    return [
        [sg.Button("Home"), sg.Text("Profile", font='bold', justification='center', expand_x=True)],
        [sg.Text("Profile info + scores will go here")],
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
window = sg.Window("Router Example", login())

# Event loop for routing
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Login":
        window.close()
        # grab user and password
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        window = sg.Window("Home", home(), finalize=True)
        # this changes the title of the window to the user's name
        # probably also how we will want to update user info through GET calls
        window['-USERNAME-DISPLAY-'].update(username + "'s Home")   

    elif event == "Profile":
        window.close()
        window = sg.Window("Profile", profile())
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
        # this is where we push information to for new record to database
        print("Term: " +  str(values['-TERM-']))
        print("Definition: " +  str(values['-DEF-']))

        window['-DEF-'].update("")
        window['-TERM-'].update("")
        window['-ADDRECORD-DISPLAY-'].update("Term " + str(values['-TERM-']) + " added!")
        

    # name = values[0]
    # password = values[1]
    
window.close()
db.close_cursor()