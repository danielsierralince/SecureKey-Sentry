import hashlib, secrets, time
import tkinter as tk
from pymongo import MongoClient

#MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["proyectoEd"]
collection = db["otp_collection"]

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

#OTP Generation
def generate_otp():
    otp = secrets.randbelow(999999) + 100000  #6-digit OTP number
    return otp

#OTP storage using a hash table
otp_table = {}

def store_otp(user):
    otp = generate_otp()
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

def abrir_ventana_otp(usuario):
    ventana_otp = tk.Toplevel()
    ventana_otp.title("Verificación de OTP")
    
    ventana_otp.geometry("200x100")
    
    label_otp = tk.Label(ventana_otp, text="Ingrese el OTP:")
    label_otp.pack()
    
    entry_otp = tk.Entry(ventana_otp)
    entry_otp.pack()
    
    def verificar_otp(usuario):
        otp = entry_otp.get()
    
        if verify_otp(usuario, otp):
            mensaje_otp.set("OTP verificado con éxito")
        else:
            mensaje_otp.set("OTP incorrecto")
    
    boton_verificar_otp = tk.Button(ventana_otp, text="Verificar OTP", command=lambda: verificar_otp(usuario))
    boton_verificar_otp.pack()
    
    mensaje_otp = tk.StringVar()
    label_mensaje_otp = tk.Label(ventana_otp, textvariable=mensaje_otp)
    label_mensaje_otp.pack()
    
    ventana_otp.mainloop()

def center_window(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

class otp_window():
    def __init__(self) -> None:
        #Window settings
        self.window = tk.Tk()
        self.window.title("SecureKey Sentry")
        center_window(self.window, 300, 150)

        #Password tag and variable
        self.password = tk.StringVar()
        password_label = tk.Label(self.window, textvariable=self.password, font=("Arial", 24))
        password_label.pack(pady=20)

        #Timer tag and variable
        self.password_label_timer = tk.StringVar()
        timer_label = tk.Label(self.window, textvariable=self.password_label_timer, font=("Arial", 12))
        timer_label.pack()

        #Timer to change password every minute
        self.user = "example_user"
        self.update_password()
        self.window.after(60000, self.update_password)

        #Starting the main loop
        self.window.mainloop()

    def countdown(self, remaining_time):
        self.password_label_timer.set("New OTP in: {} seconds".format(remaining_time))
        if remaining_time > 0:
            self.window.after(1000, self.countdown, remaining_time - 1)
    
    #Runs every minute to OTP change
    def update_password(self):
        store_otp(self.user)
        self.password.set(str(otp_table[self.user][0]))
        self.countdown(59)
        self.window.after(60000, self.update_password)  # Llamada recursiva para actualizar el OTP cada minuto

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

class main_window():
    def __init__(self):
        #Login window settup
        self.login_window = tk.Tk()
        self.login_window.title("Log in")
        center_window(self.login_window, 200, 150)

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
            self.login_window.destroy()
            otp = otp_window()
        elif collection.find_one({'user': usr}): #Password validation
            self.entry_pwd.delete(0, tk.END)
            self.message.set("Incorrect password!")
        elif not collection.find_one({'user': usr}): #User validation
            self.message.set("User doesn't exist!")

if __name__ == '__main__':
    main = main_window()