import hashlib, secrets
import tkinter as tk
from tkinter import ttk, messagebox
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

try:
    client = MongoClient(my_uri)
    data_base = client[my_db]
    collection = data_base[my_collect]
except errors.ServerSelectionTimeoutError as TimeoutError:
    print(TimeoutError)
except errors.ConnectionFailure as ConnectionError:
    print(ConnectionError)

#OTP Generation
def generate_otp():
    otp = secrets.randbelow(999999) + 100000  #6-digit OTP number
    return otp

#OTP storage using a hash table
otp_table = {}

def store_otp(user):
    otp = generate_otp()
    collection.update_one({'user': user}, {'$set': {'OTP': otp}}) #Update DB
    otp_table[user] = otp
    otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()
    otp_table[user] = (otp, otp_hash)

#OTP Verification
def verify_otp(user_id, otp):
    if user_id in otp_table:
        stored_otp, hashed_otp = otp_table[user_id]
        if hashlib.sha256(str(otp).encode()).hexdigest() == hashed_otp:
            del otp_table[user_id]
            return True
    return False

def center_window(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

class otp_window():
    def __init__(self, user) -> None:
        #Window settings
        self.window = tk.Tk()
        self.window.title("SecureKey Sentry")
        self.window.bind("<Destroy>", self.on_closing)
        center_window(self.window, 300, 160)
        try:
            self.login_window.iconbitmap("password.ico")
        except Exception:
            print(Exception)

        #Password tag and variable
        self.password = tk.StringVar()
        password_label = tk.Label(self.window, textvariable=self.password, font=("Arial", 24))
        password_label.pack(pady=20)

        #Timer tag and variable
        self.password_label_timer = tk.StringVar()
        timer_label = tk.Label(self.window, textvariable=self.password_label_timer, font=("Arial", 12))
        timer_label.pack()

        self.progressbar = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack(pady=10)

        #Timer to change password every minute
        self.user = user
        self.update_password()
        self.window.after(60000, self.update_password)

        #Starting the main loop
        self.window.mainloop()

    def countdown(self, remaining_time):
        self.password_label_timer.set("New OTP in: {} seconds".format(remaining_time))
        if remaining_time > 0:
            self.window.after(1000, self.countdown, remaining_time - 1)

    def update_progressbar(self, total_time):
        current_time = 60 - total_time
        progress = ((60 - current_time) / 60) * 100
        self.progressbar["value"] = progress
        if total_time > 0:
            self.window.after(1000, self.update_progressbar, total_time - 1)
        else:
            self.progressbar["value"] = 100
    
    #Runs every minute to OTP change
    def update_password(self):
        store_otp(self.user)
        self.password.set(str(otp_table[self.user][0]))
        self.countdown(59)
        self.update_progressbar(60)
        self.window.after(60000, self.update_password)  # Llamada recursiva para actualizar el OTP cada minuto

    def on_closing(self, event):
        #Set user inactive
        collection.update_one({'user': self.user}, {'$set': {'active': 0}})

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

class main_window():
    def __init__(self):
        #Login window settup
        self.login_window = tk.Tk()
        self.login_window.title("Log in")
        center_window(self.login_window, 200, 300)
        try:
            self.login_window.iconbitmap("password.ico")
        except Exception:
            print(Exception)

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

        #Frame for the navigation bar
        frame = tk.Frame(self.login_window, width=200, height=50, bg="black")
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12))

        back_button = ttk.Button(frame, text="◀", command=self.back_click)
        back_button.pack(side=tk.LEFT)

        start_button = ttk.Button(frame, text="🏠", command=self.start_click)
        start_button.pack(side=tk.LEFT)

        #Loop init
        self.login_window.mainloop()

    def log_in(self, event):
        #Get GUI data and data validation
        if self.entry_user.get() != "":
            usr = self.entry_user.get()
        else:
            return self.message.set("User entry is empty!")
        if self.entry_pwd.get() != "":
            pwd = md5_hash(self.entry_pwd.get())
        else:
            return self.message.set("Password entry is empty!")

        if collection.find_one({'user': usr, 'password hash': pwd}): #DB Search
            collection.update_one({'user': usr}, {'$set': {'active': 1}})
            self.login_window.destroy()
            otp = otp_window(usr)
        elif collection.find_one({'user': usr}): #Password validation
            self.entry_pwd.delete(0, tk.END)
            self.message.set("Incorrect password!")
        elif not collection.find_one({'user': usr}): #User validation
            self.message.set("User doesn't exist!")

    def back_click(arg=None):
        messagebox.showinfo("Back", "Coming back")

    def start_click(self):
        self.login_window.withdraw()
        start_window = tk.Toplevel(self.login_window)
        start_window.title("Start screen")
        try:
            screen = tk.PhotoImage(file="screen.png")
        except Exception:
            print(Exception)
        image = tk.Label(start_window, image=screen)
        image.pack()
        
        center_window(start_window, screen.width(), screen.height())
        start_window.mainloop()

if __name__ == '__main__':
    main = main_window()