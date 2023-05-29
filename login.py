import hashlib, time, tkinter as tk, json
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

def md5_hash(pwd):
    md5_hash = hashlib.md5(pwd.encode()).hexdigest()
    return md5_hash

def log_in():
    global user, entry_user, entry_pwd  #Global variables
    #Get GUI data
    usr = entry_user.get()
    pwd = md5_hash(entry_pwd.get())

    #DB Search
    db_match = False

    if db_match:
        open_window()  # Abrir la ventana del OTP
        return

def open_window():
    pass

def abrir_ventana_crear_cuenta():
    ventana_crear_cuenta = tk.Toplevel()
    ventana_crear_cuenta.title("Crear cuenta")
    ventana_crear_cuenta.geometry("300x200")
    
    label_usuario = tk.Label(ventana_crear_cuenta, text="Usuario:")
    label_usuario.pack()
    
    entry_usuario = tk.Entry(ventana_crear_cuenta)
    entry_usuario.pack()
    
    label_contrasena = tk.Label(ventana_crear_cuenta, text="Contraseña:")
    label_contrasena.pack()
    
    entry_contrasena = tk.Entry(ventana_crear_cuenta, show="*")
    entry_contrasena.pack()
    
    def guardar_cuenta():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        
        if usuario and contrasena:
            mensaje_cuenta.set("Cuenta creada con éxito")
            time.sleep(1)
            ventana_crear_cuenta.destroy()
        else:
            mensaje_cuenta.set("Por favor, ingrese usuario y contraseña")
    
    boton_guardar_cuenta = tk.Button(ventana_crear_cuenta, text="Guardar cuenta", command=guardar_cuenta)
    boton_guardar_cuenta.pack()
    
    mensaje_cuenta = tk.StringVar()
    label_mensaje_cuenta = tk.Label(ventana_crear_cuenta, textvariable=mensaje_cuenta)
    label_mensaje_cuenta.pack()

#Login window settup
login_window = tk.Tk()
login_window.title("Log in")
login_window.geometry("200x150")

label_user = tk.Label(login_window, text="User:")
label_user.pack()

entry_user = tk.Entry(login_window)
entry_user.pack()

label_pwd = tk.Label(login_window, text="Password:")
label_pwd.pack()

entry_pwd = tk.Entry(login_window, show="*")
entry_pwd.pack()

message = tk.StringVar()
label_message = tk.Label(login_window, textvariable=message)
label_message.pack()

login_button = tk.Button(login_window, text="Log in", command=log_in)
login_button.pack()

signin_button = tk.Button(login_window, text="Sign in", command=abrir_ventana_crear_cuenta)
signin_button.pack()

#Loop init
login_window.mainloop()