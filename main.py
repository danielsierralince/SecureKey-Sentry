import hashlib
import secrets

# Generación de OTP
def generate_otp():
    otp = secrets.randbelow(1000000)  # Genera un número OTP de 6 dígitos
    return otp

# Almacenamiento de OTP utilizando una tabla hash
otp_table = {}

def store_otp(user_id):
    otp = generate_otp()
    otp_table[user_id] = hashlib.sha256(str(otp).encode()).hexdigest()
    # También puedes almacenar la fecha/hora de generación y otros datos relevantes

# Verificación de OTP
def verify_otp(user_id, otp):
    if user_id in otp_table:
        stored_otp = otp_table[user_id]
        hashed_otp = hashlib.sha256(str(otp).encode()).hexdigest()
        if hashed_otp == stored_otp:
            del otp_table[user_id]
            return True
    return False