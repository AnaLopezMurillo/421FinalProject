import PySimpleGUI as sg

def login_layout():
    return [
        [sg.Text("Login Page", font='Bold', justification='center', expand_x=True)],
        [sg.Text('Username'), sg.InputText()],
        [sg.Text('Password'), sg.InputText()],
        [sg.Button("Login"), sg.Button("Exit")]
    ]

def home_layout():
    return [
        [sg.Button("Login"), sg.Text("Home Page", font='bold', justification='center', expand_x=True), sg.Button("Profile"),],
        [sg.Text("Posts will go here")],
        [sg.Button("Exit")]
    ]

def profile_layout():
    return [
        [sg.Button("Home"), sg.Text("Profile", justification='center', expand_x=True)],
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
        window.close()
        window = sg.Window("Home", home_layout())
    elif event == "Profile":
        window.close()
        window = sg.Window("Profile", profile_layout())
    elif event == "Back to Login":
        window.close()
        window = sg.Window("Login", login_layout())
    elif event == "Home":
        window.close()
        window = sg.Window("Home", home_layout())


window.close()
