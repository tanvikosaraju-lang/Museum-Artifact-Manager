import hashlib, os, hmac
from app.database import get_connection

def hash_password(password):
    salt=os.urandom(16)
    digest=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,200000)
    return salt.hex()+':'+digest.hex()

def verify_password(password,stored):
    try:
        salt,digest=stored.split(':',1)
        check=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),200000).hex()
        return hmac.compare_digest(check,digest)
    except (ValueError,TypeError):
        return False

def register_user(username,password):
    try:
        with get_connection() as c:
            c.execute("INSERT INTO users(username,password_hash) VALUES(?,?)",(username,hash_password(password)))
        return True
    except Exception:
        return False

def authenticate_user(username,password):
    with get_connection() as c:
        row=c.execute("SELECT password_hash FROM users WHERE username=?",(username,)).fetchone()
    return bool(row and verify_password(password,row[0]))
