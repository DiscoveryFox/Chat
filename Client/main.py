import tkinter
import customtkinter as tk
import webbrowser
import tkinter.font as tkfont
import re
from CustomWidgets.ListBox import ListBox
import time

WEBSITE_LINK_TO_REGISTER = 'https://youtube.de'
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
MY_ID = 101


def isValidEmail(email: str):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    else:
        return False


def isValidPassword(password: str):
    if 8 < len(password) <= 24:
        return True
    else:
        return False


def login():
    username = username_entry.get()
    password = password_entry.get()
    print(username)
    print(password)
    create_chat_app()


def fetch_messages(receiver_id):
    messages = [(101, 10, 'This is the Message Text', 1668548147.5578964),
                (10, 101, 'This is from somebody else!', 1668548243.5578964),
                (11, 101, 'This is from somebody else!', 1668548542.5578964),
                (101, 10, 'This is from somebody else!', 1668548454.5578964),
                (10, 101, 'Ecce, zeta! Lorem Ipsum The doubloons tastes with adventure, '
                          'command the bahamas until it waves.')]
    return [x for x in messages if x[0] is receiver_id or x[1] is receiver_id]


def checkUserNameEntry(Key: tkinter.Event):
    username = username_entry.get()

    if isValidEmail(username):
        username_entry.configure(True, border_color='green')
        login_button.configure(True, state=tk.NORMAL)
    else:
        username_entry.configure(True, border_color='red')
        login_button.configure(True, state=tk.DISABLED)


def checkPassWordEntry(Key: tkinter.Event):
    password = password_entry.get()
    if isValidPassword(password):
        password_entry.configure(True, border_color='green')
        login_button.configure(True, state=tk.NORMAL)
    else:
        password_entry.configure(True, border_color='red')
        login_button.configure(True, state=tk.DISABLED)


def update_chat(event: tkinter.Event):
    selection = event.widget.curselection()
    index = selection[0]
    data: str = event.widget.get(index)
    id: int = int(data.split('#')[1])
    username: str = data.split('#')[0]
    chat_label.set_text('')
    for message in fetch_messages(id):
        if message[0] == id:
            chat_label.set_text(chat_label.text + '\n' + f'[{username + "]:":20} {message[2]}')
        else:
            chat_label.set_text(chat_label.text + '\n' + f'{"[You]:":20} {message[2]}')

    print(data)


def remove_everything():
    register_link.place_forget()
    register_login_frame.place_forget()
    reg_log_entry_frame.place_forget()


def create_chat_app():
    global chat_label
    remove_everything()
    chat_app = root
    chat_app.resizable(False, False)
    chat_app.geometry('800x600')

    chat_frame = tk.CTkFrame(master=chat_app, height=590, width=590)
    friends_frame = tk.CTkFrame(master=chat_app, height=590, width=190)

    chat_label = tk.CTkLabel(master=chat_frame, justify=tk.LEFT, height=590, width=190,
                             text_font=('', 14))
    chat_label.place(relx=0.33, rely=0.5, anchor=tk.CENTER)

    chat_entry = tk.CTkEntry(master=chat_frame, height=50, width=590, text_font=('', 18))
    chat_entry.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
    # TODO: Still decide if we wanna go with textbox or entry here
    # chat_textbox = tk.CTkTextbox(master=chat_frame, height=50, width=590, text_font=('', 20))
    # chat_textbox.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    friends_listbox = tkinter.Listbox(master=friends_frame, listvariable=tkinter.Variable(
        value=get_contacts()), background='#2A2D2E', foreground='white', bd='0i',
                                      relief='flat', width=17, height=24,
                                      font=('', 15))
    # height=36, width=31,
    friends_listbox.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    friends_listbox.bind('<<ListboxSelect>>', update_chat)

    friends_frame.place(relx=0.125, rely=0.5, anchor=tk.CENTER)
    chat_frame.place(relx=0.62, rely=0.5, anchor=tk.CENTER)


def get_contacts():
    return ['tcgamer#10', 'jnb#11']


tk.set_appearance_mode('System')
tk.set_default_color_theme('blue')

root = tk.CTk()
root.title('Chat Application')
root.geometry('800x600')
root.resizable(False, False)
# Creating Fonts

big_font = tkfont.Font(size=20)

# End Creating Fonts
# Frames

register_login_frame = tk.CTkFrame(master=root, width=root.winfo_width() - 40)

reg_log_entry_frame = tk.CTkFrame(master=root, width=root.winfo_width() - 40, height=350)

# End Frames
# Buttons

login_button = tk.CTkButton(master=register_login_frame, text='Login', command=login, height=50,
                            width=200)  # , state=tk.DISABLED)
# TODO: set login_button state to tk.DISABLED again it is only commented out for testing
login_button.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

register_link = tk.CTkButton(master=register_login_frame, text='Register',
                             command=lambda: webbrowser.open_new_tab(WEBSITE_LINK_TO_REGISTER),
                             height=50,
                             width=200)

register_link.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
# End Buttons
# Entry's

username_entry = tk.CTkEntry(master=reg_log_entry_frame, width=400, height=60,
                             placeholder_text='Email/UserID', text_font=('', 20))
password_entry = tk.CTkEntry(master=reg_log_entry_frame, show='*', width=400, height=60,
                             placeholder_text='Password', text_font=('', 20))

login_label = tk.CTkLabel(master=reg_log_entry_frame, text='Login', text_font=('', 24))
# username_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
login_label.place(relx=0.5, rely=0.18, anchor=tk.CENTER)
username_entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
username_entry.bind('<KeyRelease>', checkUserNameEntry)
password_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
password_entry.bind('<KeyRelease>', checkPassWordEntry)
# End Entry's
# placing

register_login_frame.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
reg_log_entry_frame.place(relx=0.5, rely=0.33, anchor=tk.CENTER)
root.mainloop()
