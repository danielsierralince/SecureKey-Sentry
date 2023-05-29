import hashlib, time, tkinter as tk, json
from pymongo import MongoClient, errors

#MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

#My DB
my_host = "localhost"
my_port = 27017
my_uri = f"mongodb://{my_host}:{my_port}"

#DB Access
my_db = "SecureKey-Sentry"
my_collect = "Users"

client = MongoClient(my_uri)
data_base = client[my_db]
collection = data_base[my_collect]

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

def center_window(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

class otp_window():
    def __init__(self, user) -> None:
        #Window settings
        self.otp_window = tk.Tk()
        self.otp_window.title("SecureKey Sentry")
        center_window(self.otp_window, 200, 100)
        
        label_otp = tk.Label(self.otp_window, text="Enter the OTP:")
        label_otp.pack()
        
        entry_otp = tk.Entry(self.otp_window)
        entry_otp.pack()
        entry_otp.focus_set()

        button = tk.Button(self.otp_window, text="Verificar OTP", command=lambda: self.verify_otp)
        button.pack()
        
        mensaje_otp = tk.StringVar()
        label_mensaje_otp = tk.Label(self.otp_window, textvariable=mensaje_otp)
        label_mensaje_otp.pack()

        #Starting the main loop
        self.otp_window.mainloop()
    
    def verify_otp(user, otp):
        document = collection.find_one({"user_id": user})
        if document:
            hashed_otp = document["otp_hash"]
            print("OTP ingresado:", otp)  # Verificar el valor del OTP ingresado
            print("OTP almacenado:", document["otp"])  # Verificar el valor del OTP almacenado
            print("OTP hash almacenado:", hashed_otp)  # Verificar el valor del hash almacenado
            if hashlib.sha256(str(otp).encode()).hexdigest() == hashed_otp:
                collection.delete_one({"user_id": user})  # Eliminar el documento OTP verificado
                return True
        return False

class sign_in():
    def __init__(self) -> None:
        self.login_window = tk.Toplevel()
        self.login_window.title("Create an account")
        center_window(self.login_window, 300, 200)
        
        label_user = tk.Label(self.login_window, text="User:")
        label_user.pack()
        
        self.entry_user = tk.Entry(self.login_window)
        self.entry_user.pack()
        
        label_pwd = tk.Label(self.login_window, text="Password:")
        label_pwd.pack()
        
        self.entry_pwd = tk.Entry(self.login_window, show="*")
        self.entry_pwd.pack()

        button = tk.Button(self.login_window, text="Save account", command=self.save_account)
        button.pack()
        
        message = tk.StringVar()
        label_message = tk.Label(self.login_window, textvariable=message)
        label_message.pack()
    
    def save_account(self):
        if self.entry_user.get() != "":
            user = self.entry_user.get()
        else:
            return self.message.set("User entry is empty!")
        if self.entry_pwd.get() != "":
            password = md5_hash(self.entry_pwd.get())
        else:
            return self.message.set("Password entry is empty!")
        
        try:
            document = {
                'user': user,
                'password hash': password,
                'OTP': 000000,
                'active': 0
            }
            collection.insert_one(document)
        except errors.ServerSelectionTimeoutError as TimeoutError:
            print(TimeoutError)
        except errors.ConnectionFailure as ConnectionError:
            print(ConnectionError)

        self.open_popup()
        self.login_window.destroy()
    
    def open_popup():
        popup_window = tk.Toplevel()
        popup_window.title("Saved")
        center_window(popup_window, 200, 100)

        label = tk.Label(popup_window, text="The user was successfully added!")
        label.pack(pady=20)

        button = tk.Button(popup_window, text="Okay", command=popup_window.destroy)
        button.pack()

def sign_in():
    sign_in = sign_in()

class login_window():
    def __init__(self):
        #Login window settup
        self.login_window = tk.Tk()
        self.login_window.title("Log in")
        center_window(self.login_window, 200, 170)

        label_user = tk.Label(self.login_window, text="User:")
        label_user.pack()

        self.entry_user = tk.Entry(self.login_window)
        self.entry_user.pack()
        self.entry_user.focus_set()
        self.entry_user.bind('<Return>', self.log_in)

        label_pwd = tk.Label(self.login_window, text="Password:")
        label_pwd.pack()

        self.entry_pwd = tk.Entry(self.login_window, show="*")
        self.entry_pwd.pack()
        self.entry_pwd.bind('<Return>', self.log_in)

        self.message = tk.StringVar()
        label_message = tk.Label(self.login_window, textvariable=self.message)
        label_message.pack()

        login_button = tk.Button(self.login_window, text="Log in", command=self.log_in)
        login_button.pack()

        signin_button = tk.Button(self.login_window, text="Sign in", command=sign_in)
        signin_button.pack()

        #Loop init
        self.login_window.mainloop()

    def log_in(self, event=None):
        #Get GUI data and data validation
        if self.entry_user.get() != "":
            usr = self.entry_user.get()
        else:
            return self.message.set("User entry is empty!")
        if self.entry_pwd.get() != "":
            pwd = md5_hash(self.entry_pwd.get())
        else:
            return self.message.set("Password entry is empty!")
        
        #Active OTP generator
        access = collection.find_one({'user': usr, 'active': 1})

        if collection.find_one({'user': usr, 'password hash': pwd}) and access: #DB Search
            self.login_window.destroy()
            otp = otp_window(usr)
        elif collection.find_one({'user': usr, 'password hash': pwd}) and not access:
            self.message.set("The user isn't active in the platform!")
        elif collection.find_one({'user': usr}): #Password validation
            self.entry_pwd.delete(0, tk.END)
            self.message.set("Incorrect password!")
        elif not collection.find_one({'user': usr}): #User validation
            self.message.set("User doesn't exist!")

if __name__ == '__main__':
    main = login_window()