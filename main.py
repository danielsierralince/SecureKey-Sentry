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

OTP = 0

#OTP Generation
def generate_otp():
    otp = secrets.randbelow(999999) + 100000  #6-digit OTP number
    return otp

#OTP storage using a hash table
otp_table = {}

def store_otp(user_id):
    otp = generate_otp()
    otp_table[user_id] = otp
    otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()
    otp_table[user_id] = (otp, otp_hash)

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

def countdown(remaining_time):
    password_label_timer.set("Updating OTP en: {} segundos".format(remaining_time))
    if remaining_time > 0:
        window.after(1000, countdown, remaining_time - 1)

#Runs every minute to OTP change
def update_password(user):
    store_otp(user)
    password.set(str(otp_table[user][0]))
    countdown(60)
    window.after(60000, update_password)  # Llamada recursiva para actualizar el OTP cada minuto

#Window settings
window = tk.Tk()
window.title("SecureKey Sentry")
window.geometry("300x200")

#Password tag and variable
password_label_timer = tk.StringVar()
password = tk.StringVar()
password_label = tk.Label(window, textvariable=password, font=("Arial", 24))
password_label.pack(pady=20)

#First password
user = "example_user"
store_otp(user)
password.set(str(otp_table[user][0]))

#Timer to change password every minute
window.after(60000, update_password)

#Starting the main loop
window.mainloop()

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

class main_window():
    def __init__(self):
        #Login window settup
        login_window = tk.Tk()
        login_window.title("Log in")
        login_window.geometry("200x150")

        label_user = tk.Label(login_window, text="User:")
        label_user.pack()

        self.entry_user = tk.Entry(login_window)
        self.entry_user.pack()

        label_pwd = tk.Label(login_window, text="Password:")
        label_pwd.pack()

        self.entry_pwd = tk.Entry(login_window, show="*")
        self.entry_pwd.pack()

        self.message = tk.StringVar()
        label_message = tk.Label(login_window, textvariable=self.message)
        label_message.pack()

        login_button = tk.Button(login_window, text="Log in", command=self.log_in)
        login_button.pack()

        #Loop init
        login_window.mainloop()

    def log_in(self):
        #Get GUI data
        usr = self.entry_user.get()
        pwd = md5_hash(self.entry_pwd.get())

        if collection.find_one({'user': usr, 'password hash': pwd}): #DB Search
            self.message.set("Access granted!")
        elif collection.find_one({'user': usr}): #Password validation
            self.message.set("Incorrect password!")
        elif not collection.find_one({'user': usr, 'password hash': pwd}): #User validation
            self.message.set("User doesn't exist!")