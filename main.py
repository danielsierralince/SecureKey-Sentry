import hashlib
import secrets
import time
import tkinter as tk

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

#Runs every minute to OTP change
def update_password():
    store_otp(user)
    password.set(str(otp_table[user][0]))

#Window settings
window = tk.Tk()
window.title("SecureKey Sentry")
window.geometry("300x200")

#Password tag and variable
password = tk.StringVar()
password_label = tk.Label(window, textvariable=password, font=("Arial", 24))
password_label.pack(pady=20)

#First password
user = "example_user"
store_otp(user)
password.set(str(otp_table[user]))

#Timer to change password every minute
window.after(60000, update_password)

#Starting the main loop
window.mainloop()