import PySimpleGUI as sg
import db

cursor = db.get_cursor()

# vars
username = ''
password = ''

def login_layout():
    return [
        [sg.Text("Login Page", font='Bold', justification='center', expand_x=True)],
        [sg.Text('Username'), sg.InputText(key='-USERNAME-')],
        [sg.Text('Password'), sg.InputText(password_char='*', key='-PASSWORD-')],
        [sg.Button("Exit"), sg.Text("", expand_x=True), sg.Button("Login")]
    ]

def home_layout():
    return [
        [sg.Button("Back to Login"), sg.Text("", key='-USERNAME-DISPLAY-', font='bold', justification='center', expand_x=True), sg.Button("Profile"),],
        [sg.Text("Posts will go here")],
        [sg.Button("Exit")]
    ]

def profile_layout():
    return [
        [sg.Button("Home"), sg.Text("Profile", font='bold', justification='center', expand_x=True)],
        [sg.Text("Profile info + scores will go here")],
        [sg.Button("Exit")]
    ]

# Set the initial window with the main layout
window = sg.Window("Router Example", login_layout())


# Event loop for routing
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Login":
        # grab user and password
        username = values['-USERNAME-']
        password = values['-PASSWORD-']

        window.close()
        window = sg.Window("Home", home_layout(), finalize=True)
        window['-USERNAME-DISPLAY-'].update(username + "'s Home")   # this changes the title of the window to the user's name

    elif event == "Profile":
        window.close()
        window = sg.Window("Profile", profile_layout())
    elif event == "Back to Login":
        window.close()
        window = sg.Window("Login", login_layout())
    elif event == "Home":
        window.close()
        window = sg.Window("Home", home_layout(), finalize=True)
        window['-USERNAME-DISPLAY-'].update(username + "'s Home")

    # name = values[0]
    # password = values[1]
    
window.close()
db.close_cursor()