import hashlib, tkinter as tk, random
from tkinter import messagebox
from pymongo import MongoClient, errors
from PIL import ImageTk, Image

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

def hash(cc):
    table_size = 100  #Table hash size

    #Folding technique
    groups = [int(cc[i:i+2]) for i in range(0, len(cc), 2)] #Divide the number

    total = sum(groups) #Add

    hash_value = total % table_size #Size module

    probe = 1
    #Quadratic probing in case of collision
    while not collection.find_one({"_id": hash_value, "user": None}):
        #Open addressing technique 'quadratic probing'
        hash_value = (hash_value + probe**2) % table_size #Rehashing, position with quadratic test
        probe += 1
        if probe==100:
            return 1000

    return hash_value

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

def center_window(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

class bank_window():
    def __init__(self) -> None:
        #Window settings
        bank_window = tk.Tk()
        bank_window.title("Bank")
        bank_window.geometry("300x200")
        center_window(bank_window, 300, 200)
        try:
            self.login_window.iconbitmap("bank.ico")
        except Exception:
            print(Exception)

        try:
            bank_window.iconbitmap("card.png")
            card_image = Image.open("card.png")
        except Exception:
            print(Exception)
        card_image = card_image.resize((100, 100))  #Adjust image
        card_image = ImageTk.PhotoImage(card_image)

        label_amount = tk.Label(bank_window, text="Enter the amount to withdraw:", font=("Arial", 12), bg="#d0f2a0", fg="black", padx=10, pady=5)
        label_amount.pack()

        self.entry_amount = tk.Entry(bank_window)
        self.entry_amount.pack()

        boton_withdraw = tk.Button(bank_window, text="Withdraw", command=self.make_withdrawal, bg="#c95824", fg="white", font=("Arial", 12), relief=tk.RAISED)
        boton_withdraw.pack()

        self.available_balance = self.generate_balance()
        label_saldo = tk.Label(bank_window, text=f"Available balance: {self.available_balance} USD", font=("Arial", 10), bg="#d0f2a0", fg="black", padx=10, pady=5)
        label_saldo.pack()
        label_imagen = tk.Label(bank_window, image=card_image)
        label_imagen.pack()

        bank_window.mainloop()

    def make_withdrawal(self):
        amount = self.entry_amount.get()
        if amount.isdigit():
            amount = int(amount)
            if amount <= self.available_balance:
                messagebox.showinfo("Bank", f"Successful withdrawal! {amount} dollars withdrew")
            else:
                messagebox.showerror("Bank", "Insufficient balance. The withdrawal cannot be made!")
        else:
            messagebox.showerror("Bank", "Invalid amount. Enter a numeric value!")

    def generate_balance(self):
        balances = [500, 1350, 2300, 10000, 20000, 25000, 37000, 48000, 52000, 79000, 94000, 103000, 256000, 512000]
        return random.choice(balances)

class otp_window():
    def __init__(self, user) -> None:
        self.user = user

        #Window settings
        self.otp_window = tk.Tk()
        self.otp_window.title("SecureKey Sentry")
        center_window(self.otp_window, 200, 100)
        try:
            self.otp_window.iconbitmap("sentry-gun.ico")
        except Exception:
            print(Exception)
        
        label_otp = tk.Label(self.otp_window, text="Enter the OTP:")
        label_otp.pack()
        
        self.entry_otp = tk.Entry(self.otp_window)
        self.entry_otp.pack()
        self.entry_otp.focus_set()
        self.entry_otp.bind('<Return>', self.verify_otp)

        self.message = tk.StringVar()
        label_mensaje_otp = tk.Label(self.otp_window, textvariable=self.message)
        label_mensaje_otp.pack()

        button = tk.Button(self.otp_window, text="Verificar OTP", command=lambda: self.verify_otp)
        button.pack()

        #Starting the main loop
        self.otp_window.mainloop()
    
    def verify_otp(self, agr=None):
        otp = self.entry_otp.get()
        if collection.find_one({"user": self.user, "OTP": int(otp)}):
            self.otp_window.destroy()
            bank = bank_window()
        elif collection.find_one({"user": self.user}):
            return self.message.set("Invalid OTP!")

class sign_in():
    def __init__(self) -> None:
        self.login_window = tk.Tk()
        self.login_window.title("Create an account")
        center_window(self.login_window, 200, 170)
        try:
            self.login_window.iconbitmap("sentry-gun.ico")
        except Exception:
            print(Exception)
        
        label_user = tk.Label(self.login_window, text="User:")
        label_user.pack()
        
        self.entry_user = tk.Entry(self.login_window)
        self.entry_user.pack()
        self.entry_user.focus_set()
        self.entry_user.bind('<Return>', self.save_account)

        label_cc = tk.Label(self.login_window, text="Identification card:")
        label_cc.pack()
        
        self.entry_cc = tk.Entry(self.login_window)
        self.entry_cc.pack()
        self.entry_cc.bind('<Return>', self.save_account)
        
        label_pwd = tk.Label(self.login_window, text="Password:")
        label_pwd.pack()
        
        self.entry_pwd = tk.Entry(self.login_window, show="*")
        self.entry_pwd.pack()
        self.entry_pwd.bind('<Return>', self.save_account)

        self.label_message = tk.Label(self.login_window, text="")
        self.label_message.pack()

        button = tk.Button(self.login_window, text="Save account", command=self.save_account)
        button.pack()

        #Loop init
        self.login_window.mainloop()
    
    def insert_db(self, user, password, cc):
        try:
            id = hash(cc)
            if id != 1000:
                collection.update_one({"_id": id}, {'$set': {'user': user, 'password hash': password, "Cc": cc}})
            else:
                self.text_label("DB is fill! Contact developer!")
        except errors.ServerSelectionTimeoutError as TimeoutError:
            print(TimeoutError)
        except errors.ConnectionFailure as ConnectionError:
            print(ConnectionError)
        
        self.open_popup(id)
    
    def text_label(self, set_text):
        self.label_message.config(text=set_text)
    
    def save_account(self, arg=None):
        user = self.entry_user.get()
        if user != "" and not collection.find_one({'user': user}):
            user = self.entry_user.get()
        elif collection.find_one({'user': user}):
            return self.text_label("The user already exists!")
        else:
            return self.text_label("User entry is empty!")
        
        if self.entry_pwd.get() != "":
            password = md5_hash(self.entry_pwd.get())
        else:
            return self.text_label("Password entry is empty!")
        
        if self.entry_cc.get() != "":
            cc = self.entry_cc.get()
        else:
            return self.text_label("ID card entry is empty!")
        if len(self.entry_cc.get()) != 10:
            return self.text_label("UD card must have 10 digits!")
        
        self.insert_db(user, password, cc)
        self.login_window.destroy()
    
    def open_popup(self, id):
        self.popup_window = tk.Tk()
        self.popup_window.title("Saved")
        center_window(self.popup_window, 200, 100)
        try:
            self.popup_window.iconbitmap("sentry-gun.ico")
        except Exception:
            print(Exception)

        tex = f"The user was successfully added!\nID: {id}"
        label = tk.Label(self.popup_window, text=tex)
        label.pack(pady=20)

        button = tk.Button(self.popup_window, text="Okay", command=self.close_popup)
        button.pack()

    def close_popup(self):
        self.popup_window.destroy()

class login_window():
    def __init__(self):
        #Login window settup
        self.login_window = tk.Tk()
        self.login_window.title("Log in")
        center_window(self.login_window, 200, 170)
        try:
            self.login_window.iconbitmap("sentry-gun.ico")
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

        signin_button = tk.Button(self.login_window, text="Sign in", command=self.sign_in)
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
    
    def sign_in(self):
        signin = sign_in()
        self.login_window.destroy()

if __name__ == '__main__':
    main = login_window()