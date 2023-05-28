import hashlib
import secrets
import time
import tkinter as tk

# Generación de OTP
def generate_otp():
    otp = secrets.randbelow(999999) + 100000  # Genera un número OTP de 6 dígitos
    return otp

# Almacenamiento de OTP utilizando una tabla hash
otp_table = {}

def store_otp(user_id):
    otp = generate_otp()
    otp_table[user_id] = otp
    otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()
    otp_table[user_id] = (otp, otp_hash) 
    # También puedes almacenar la fecha/hora de generación y otros datos relevantes

# Verificación de OTP
def verify_otp(user_id, otp):
    if user_id in otp_table:
        stored_otp, hashed_otp = otp_table[user_id]
        if hashlib.sha256(str(otp).encode()).hexdigest() == hashed_otp:
            del otp_table[user_id]
            return True
    return False

# Función que se ejecuta cada minuto para cambiar la contraseña
def update_password():
    store_otp(user_id)
    password.set(str(otp_table[user_id][0]))

# Configuración de la ventana
window = tk.Tk()
window.title("One Time Password")
window.geometry("300x200")

# Configuración de la etiqueta y la variable de contraseña
password = tk.StringVar()
password_label = tk.Label(window, textvariable=password, font=("Arial", 24))
password_label.pack(pady=20)

# Generación de la primera contraseña
user_id = "example_user"
store_otp(user_id)
password.set(str(otp_table[user_id]))

# Configuración del temporizador para cambiar la contraseña cada minuto
window.after(60000, update_password)

# Inicio del bucle principal de la ventana
window.mainloop()

def iniciar_sesion():
    # Obtener los valores ingresados por el usuario
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    # Realizar la verificación de inicio de sesión aquí
    if usuario == "user" and contrasena == "password":
        mensaje.set("Inicio de sesión exitoso")
        store_otp(usuario)  # Almacenar OTP para el usuario
        window.withdraw()  # Ocultar la primera ventana
        abrir_ventana_otp(usuario)  # Abrir la ventana del OTP
    if usuario != "user":
        mensaje.set("Usuario incorrecto")
    if contrasena != "password":
        mensaje.set("Contraseña incorrecta")

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


# Configuración de la ventana
window = tk.Tk()
window.title("Iniciar sesión")

# Tamaño de la ventana
window.geometry("200x150")

# Etiqueta y campo de entrada para el usuario
label_usuario = tk.Label(window, text="Usuario:")
label_usuario.pack()
entry_usuario = tk.Entry(window)
entry_usuario.pack()

# Etiqueta y campo de entrada para la contraseña
label_contrasena = tk.Label(window, text="Contraseña:")
label_contrasena.pack()
entry_contrasena = tk.Entry(window, show="*")  # Para ocultar la contraseña
entry_contrasena.pack()

# Botón de inicio de sesión
boton_iniciar_sesion = tk.Button(window, text="Iniciar sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack()

# Variable para mostrar el mensaje de inicio de sesión
mensaje = tk.StringVar()
label_mensaje = tk.Label(window, textvariable=mensaje)
label_mensaje.pack()

# Inicio del bucle principal de la ventana
window.mainloop()