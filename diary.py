from tkinter.messagebox import showerror, showinfo
import hashlib, datetime, csv, sys
import customtkinter as ctk
import tkinter as tk
import os


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

os.makedirs('data', exist_ok=True) 

class App(ctk.CTk):

    def __init__(self, password, username):
        super().__init__()

        # Set focus and get username and password from login window      
        self.password = password
        self.username = username

        # Initialize app window
        self.focus_force()
        self.geometry('700x540')
        self.title('Dear Diary')
        self.resizable(False, False)

        # Greeting from Mia
        self.greeting = ctk.CTkLabel(self, text='Hello, how are you today?')
        self.greeting.config(font=('TkDefaultFont', 14))
        self.greeting.place(relx=0.5, y=20, anchor=tk.CENTER)

        # Text area
        self.entry = ctk.CTkTextbox(self, wrap=tk.WORD, width=650, height=440)
        self.entry.textbox.config(font=('TkDefaultFont', 12))
        self.entry.textbox.bind('<Control-d>', self.add_date_event)
        self.entry.textbox.bind('<Control-s>', self.save_dairy_event)
        self.entry.place(x=25, y=40)

        # Open database and write diary to text area
        if not os.path.isfile(f'data/{self.username}_diary.txt'):
            pass
        else:
            with open(f"data/{self.username}_diary.txt", mode='r') as file:
                content = self.decrypt(file.read())
                self.entry.insert(tk.END, content)

        # Scroll to the bottom and set the cursor at the end
        self.entry.textbox.see('end')
        self.entry.focus_set()

        # Save diary button
        self.save_diary_button = ctk.CTkButton(self, text='Save Diary (Ctrl+S)', height=25, command=self.save_diary)
        self.save_diary_button.place(relx=0.25, y=510, anchor=tk.CENTER)
        # Add date button
        self.add_date_button = ctk.CTkButton(self, text='Add date (Ctrl+D)', height=25, command=self.add_date)
        self.add_date_button.place(relx=0.5, y=510, anchor=tk.CENTER)
        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text='Cancel', height=25, command=self.cancel)
        self.cancel_button.place(relx=0.75, y=510, anchor=tk.CENTER)


    def cancel(self):
        sys.exit()

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
        with open(f"data/{self.username}_diary.txt", mode='w') as file:
            content = self.encrypt(self.entry.textbox.get('1.0', 'end') + '\n')
            file.write(content)

        # Notification after successfully saved diary
        showinfo(title='Saved', message='New entry has been saved.')
        
    def add_date(self):
        """
        Add date for every entry in diary
        """
        # Get today's date
        today = datetime.datetime.strftime(datetime.datetime.now(), '%A %B-%d-%Y')

        # Insert today into text are
        self.entry.insert(tk.END, f"  --------------------------------------------{today}------------------------------------------\n")
        
        # Scroll to the end and set the cursor there
        self.entry.textbox.see('end')
        self.entry.textbox.focus_set()


class Register(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Initialize login form
        self.geometry('300x430')
        self.title('Register')
        self.resizable(False, False)

        # Form header
        self.header = ctk.CTkLabel(self, text='Create new user')
        self.header.config(font=('TkDefaultFont', 18))
        self.header.place(relx=0.5, y=80, anchor=tk.CENTER)

        # Username entry
        self.username_entry = ctk.CTkEntry(self, width=180, placeholder_text='Username')
        self.username_entry.focus_set()
        self.username_entry.place(relx=0.5, y=150, anchor=tk.CENTER)

        # Password entry
        self.password1_entry = ctk.CTkEntry(self, placeholder_text='Password',width=180, show='*')
        self.password1_entry.place(relx=0.5, y=190, anchor=tk.CENTER)

        #Re-enter password
        self.password2_entry = ctk.CTkEntry(self, width=180, placeholder_text='Re-enter password', show='*')
        self.password2_entry.bind('<Return>', self.create_enter)
        self.password2_entry.place(relx=0.5, y=230, anchor=tk.CENTER)

        # Login button
        create_button = ctk.CTkButton(self, text='Create User', height=25, command=self.create)
        create_button.place(relx=0.5, y=310, anchor=tk.CENTER)
        # Cancel button
        cancel_button = ctk.CTkButton(self, text='Cancel', height=25, command=self.cancel)
        cancel_button.place(relx=0.5, y=345, anchor=tk.CENTER)

        #Copyright label
        copyright = ctk.CTkLabel(self, text='Made by Eric | \u00a9 2022')
        copyright.place(relx=0.5, y=420, anchor=tk.CENTER)

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
                with open('data/database.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.row)
                showinfo(title='Registered', message='New user has been added.')
                self.cancel()

    def cancel(self):
        
        login.deiconify()
        self.withdraw()


class Login(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Initialize login form
        self.geometry('300x430')
        self.title('Login')
        self.resizable(False, False)

        # Form header
        self.header = ctk.CTkLabel(self, text='DEAR DIARY', text_font=('', 24))
        self.header.place(relx=0.5, y=100, anchor=tk.CENTER)

        # Username entry
        self.username_entry = ctk.CTkEntry(self,placeholder_text='Username', width=180)
        self.username_entry.focus_set()
        self.username_entry.place(relx=0.5, y=160, anchor=tk.CENTER)

        # Password entry
        self.password_entry = ctk.CTkEntry(self, placeholder_text='Password', width=180, show='*')
        self.password_entry.bind('<Return>', self.validate_enter)
        self.password_entry.place(relx=0.5, y=200, anchor=tk.CENTER)

        # Login button
        login_button = ctk.CTkButton(self, text='Log in', height=25, command=self.validate)
        login_button.place(relx=0.5, y=270, anchor=tk.CENTER)
        # Register button
        register_button = ctk.CTkButton(self, text='Create User', height=25, command=self.create_user)
        register_button.place(relx=0.5, y=310, anchor=tk.CENTER)
        # Cancel button
        cancel_button = ctk.CTkButton(self, text='Cancel', height=25, command=self.cancel)
        cancel_button.place(relx=0.5, y=350, anchor=tk.CENTER)

        #Copyright label
        copyright = ctk.CTkLabel(self, text='Made by Eric | \u00a9 2022')
        copyright.place(relx=0.5, y=420, anchor=tk.CENTER)

    def cancel(self):
        sys.exit()

    def create_user(self):
        self.withdraw()
        new_user = Register()
        new_user.mainloop()
        

    def validate_enter(self, event):
        # Redirect to validate function
        self.validate()

    def validate(self):
        """
        Validate log in credentials
        """
        # Get username and password from text field
        self.u = self.username_entry.get()
        self.p = self.password_entry.get()

        # Error message if username field is blank
        if not self.u:
            showerror(title='Error', message='Please enter username.')
            self.username_entry.focus_set()

        # Error message if password field is blank
        elif not self.p:
            showerror(title='Error', message='Please enter password')
            self.password_entry.focus_set()

        else:
            if not os.path.isfile('data/database.csv'):
                showinfo(title='Empty database', message='No account in database, please create new user.')
                self.username_entry.delete(0, 20)
                self.password_entry.delete(0, 20)

            else:
                if os.path.getsize('data/database.csv') > 0:
                    hashed_password = hashlib.md5(self.p.encode()).hexdigest()

                    with open('data/database.csv', mode='r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if self.u == row[0] and hashed_password == row[1]:
                                self.open_app()
                        showerror(title='Error', message='Username or password not valid')
                        self.username_entry.delete(0, 20)
                        self.password_entry.delete(0, 20)
                        self.username_entry.focus_set()
                else:
                    showerror(title='Empty database', message='No account in databse, please create new user')


    def open_app(self):
        self.withdraw()
        app = App(self.p, self.u)
        app.mainloop()
        

login = Login()
login.mainloop()
