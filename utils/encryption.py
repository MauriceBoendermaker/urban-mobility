from cryptography.fernet import Fernet
import hashlib
import os

KEY_FILE = "logs/logkey.key"


# Generate de encryption key 1x (gebruik generate_key.py om deze te genereren)
def generate_key():
    key = Fernet.generate_key()
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        raise Exception("Encryption key niet gevonden: run eerst generate_key().")
    with open(KEY_FILE, "rb") as f:
        return f.read()


# Method om een string te encrypten
def encrypt(plain_text: str) -> str:
    fernet = Fernet(load_key())
    return fernet.encrypt(plain_text.encode()).decode()


# Method om een string te decrypten
def decrypt(encrypted_text: str) -> str:
    fernet = Fernet(load_key())
    return fernet.decrypt(encrypted_text.encode()).decode()


# SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
