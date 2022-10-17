from tkinter.messagebox import showerror, showinfo
import hashlib, datetime, csv
import tkinter as tk
import os.path

from requests import delete


class App(tk.Tk):

    def __init__(self, password, username):
        super().__init__()

        # Set focus and get username and password from login window
        self.focus_force()       
        self.password = password
        self.username = username

        # Initialize app window
        self.geometry('700x530')
        self.title('Dear Diary')
        self.resizable(False, False)

        # Greeting from Mia
        self.greeting = tk.Label(self, text='Hello, how are you today?')
        self.greeting.config(font=('TkDefaultFont', 14))
        self.greeting.place(x=220, y=10)

        # Text area
        self.entry = tk.Text(self, wrap=tk.WORD, width=82, height=25)
        self.entry.bind('<Control-d>', self.add_date_event)
        self.entry.bind('<Control-s>', self.save_dairy_event)
        self.entry.place(x=20, y=45)

        # Open database and write diary to text area
        if not os.path.isfile(f'{self.username}_diary.txt'):
            pass
        else:
            with open(f"{self.username}_diary.txt", mode='r') as file:
                content = self.decrypt(file.read())
                self.entry.insert(tk.END, content)

        # Scroll to the bottom and set the cursor at the end
        self.entry.see('end')
        self.entry.focus_force()

        # Save diary button
        self.save_diary_button = tk.Button(self, text='Save Diary (Ctrl+S)', height=2, width=25, command=self.save_diary)
        self.save_diary_button.place(x=160, y=470)
        # Add date button
        self.add_date_button = tk.Button(self, text='Add date (Ctrl+D)', height=2, width=25, command=self.add_date)
        self.add_date_button.place(x=360, y=470)

    def add_date_event(self, event):
        """
        Add date shortcut
        """
        # Redirect to add_date function
        self.add_date()

    def save_dairy_event(self, event):
        """
        Save diary shortcut
        """
        # Redirect to save_diary function
        self.save_diary()

    def encrypt(self, text):
        """
        Encrypt diary according to your password
        """
        key = [ord(char) for char in self.password]
        encrypted = '$'.join([str(ord(text[i]) - key[i % len(key)]) for i in range(len(text))])
        return encrypted

    def decrypt(self, text):
        """
        Decrypt diary according to your password
        """
        key = [ord(char) for char in self.password]
        if text:
            temp = text.split('$')
            decrypted = ''.join([chr(int(temp[i]) + key[i % len(key)]) for i in range(len(temp))])
            return decrypted
        else:
            return ''
            
    def save_diary(self):
        """
        Encrypt diary and save to file
        """
        # Open file and save entry
        with open(f"{self.username}_diary.txt", mode='w') as file:
            content = self.encrypt(self.entry.get('1.0', 'end'))
            file.write(content)

        # Notification after successfully saved diary
        showinfo(title='Saved', message='New entry has been saved.')
        
    def add_date(self):
        """
        Add date for every entry in diary
        """
        # Get today's date
        today = datetime.datetime.strftime(datetime.datetime.now(), '%a %b-%d-%y')

        # Insert today into text are
        self.entry.insert(tk.END, f"----------------------------------{today}-----------------------------------\n")
        
        # Scroll to the end and set the cursor there
        self.entry.see('end')
        self.entry.focus_set()


class Register(tk.Tk):

    def __init__(self):
        super().__init__()

        # Initialize login form
        self.geometry('300x400')
        self.title('Register')
        self.resizable(False, False)

        # Form header
        self.header = tk.Label(self, text='Create new user')
        self.header.config(font=('TkDefaultFont', 18))
        self.header.place(x=60, y=52)

        # Username entry
        self.username = tk.StringVar()
        self.username_label = tk.Label(self, text='Username:')
        self.username_label.place(x=40, y=130)
        self.username_entry = tk.Entry(self, textvariable=self.username)
        self.username_entry.focus_set()
        self.username_entry.place(x=130, y=130)

        # Password entry
        self.password1 = tk.StringVar()
        self.password1_label = tk.Label(self, text='Password:')
        self.password1_label.place(x=40, y=170)
        self.password1_entry = tk.Entry(self, textvariable=self.password1, show='*')
        self.password1_entry.place(x=130, y=170)

        #Re-enter password
        self.password2 = tk.StringVar()
        self.password2_label = tk.Label(self, text='Re-enter Pass:')
        self.password2_label.place(x=40, y=210)
        self.password2_entry = tk.Entry(self, textvariable=self.password2, show='*')
        self.password2_entry.bind('<Return>', self.create_enter)
        self.password2_entry.place(x=130, y=210)

        # Login button
        create_button = tk.Button(self, text='Create User', height=2, width=18, command=self.create)
        create_button.place(x=85, y=270)
        # Cancel button
        cancel_button = tk.Button(self, text='Cancel', height=2, width=18, command=self.cancel)
        cancel_button.place(x=85, y=320)

    def create_enter(self, event):
        self.create()

    def create(self):
        self.u = self.username_entry.get()
        self.p1 = self.password1_entry.get()
        self.p2 = self.password2_entry.get()

        if not self.u:
            showerror(title='Error', message='Please enter username.')
            self.username_entry.focus_set()
        elif not self.p1:
            showerror(title='Error', message='Please enter password.')
            self.password1_entry.focus_set()
        elif not self.p2:
            showerror(title='Error', message='Please re-enter password.')
            self.password2_entry.focus_set()
        else:
            if self.p1 != self.p2:
                showerror(title='Error', message='Password do not match, please try again.')
                self.password1_entry.delete(0, 20)
                self.password2_entry.delete(0, 20)
                self.password1_entry.focus_set()
            else:
                self.hash = hashlib.md5(self.p1.encode()).hexdigest()
                self.row = [self.u, self.hash]
                with open('database.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.row)
                showinfo(title='Registered', message='New user has been added.')
                self.cancel()

    def cancel(self):
        self.destroy()
        login = Login()
        login.focus_force()

class Login(tk.Tk):

    def __init__(self):
        super().__init__()

        self.focus_force()
        # Initialize login form
        self.geometry('300x400')
        self.title('Login')
        self.resizable(False, False)

        # Form header
        self.header = tk.Label(self, text='DEAR DIARY')
        self.header.config(font=('TkDefaultFont', 24))
        self.header.place(x=53, y=52)

        # Username entry
        self.username = tk.StringVar()
        self.username_label = tk.Label(self, text='Username:')
        self.username_label.place(x=50, y=150)
        self.username_entry = tk.Entry(self, textvariable=self.username)
        self.username_entry.focus_set()
        self.username_entry.place(x=120, y=150)

        # Password entry
        self.password = tk.StringVar()
        self.password_label = tk.Label(self, text='Password:')
        self.password_label.place(x=50, y=190)
        self.password_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.bind('<Return>', self.validate_enter)
        self.password_entry.place(x=120, y=190)

        # Login button
        login_button = tk.Button(self, text='Log in', height=2, width=18, command=self.validate)
        login_button.place(x=85, y=270)
        # Cancel button
        register_button = tk.Button(self, text='Create User', height=2, width=18, command=self.create_user)
        register_button.place(x=85, y=320)

    def create_user(self):
        new_user = Register()
        new_user.focus_force()
        self.destroy()

    def validate_enter(self, event):
        # Redirect to validate function
        self.validate()

    def validate(self):
        """
        Validate log in credentials
        """
        # Get username and password from text field
        self.u = self.username.get()
        self.p = self.password.get()

        # Error message if username field is blank
        if not self.u:
            showerror(title='Error', message='Please enter username.')
            self.username_entry.focus_set()

        # Error message if password field is blank
        elif not self.p:
            showerror(title='Error', message='Please enter password')
            self.password_entry.focus_set()

        else:
            if not os.path.isfile('database.csv'):
                showinfo(title='Empty database', message='No account in database, please create new user.')
                self.username_entry.delete(0, 20)
                self.password_entry.delete(0, 20)

            else:
                if os.path.getsize('database.csv') > 0:
                    hashed_password = hashlib.md5(self.p.encode()).hexdigest()

                    with open('database.csv', mode='r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if self.u == row[0] and hashed_password == row[1]:
                                self.open_app()
                            else:
                                showerror(title='Error', message='Username or password not valid')
                                self.username_entry.delete(0, 20)
                                self.password_entry.delete(0, 20)
                                self.username_entry.focus_set()
                else:
                    showerror(title='Empty database', message='No account in databse, please create new user')


    def open_app(self):
        self.destroy()
        app = App(self.p, self.u)
        

login = Login()
login.mainloop()
