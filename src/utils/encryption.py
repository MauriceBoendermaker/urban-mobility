import os
import base64
import hashlib
import secrets

from Crypto.Cipher import AES
from dotenv import load_dotenv
from cryptography.fernet import Fernet

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(CURRENT_DIR, "Key.env")
load_dotenv(dotenv_path)

KEY_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "..", "logs", "logkey.key"))

# Load and decode the encryption key
key_b64 = os.getenv("ENCRYPTION_KEY")
if key_b64 is None:
    raise ValueError("Missing DETERMINISTIC_ENCRYPTION_KEY in environment")

DETERMINISTIC_ENCRYPTION_KEY = base64.b64decode(key_b64)


def deterministic_encrypt(plaintext) -> str:
    if plaintext is None:
        return ""
    plaintext = str(plaintext)  # Convert int, float, bool, etc. to string
    cipher = AES.new(DETERMINISTIC_ENCRYPTION_KEY, AES.MODE_SIV)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return (ciphertext + tag).hex()


def deterministic_decrypt(ciphertext_hex) -> str:
    if not ciphertext_hex:
        return ""
    data = bytes.fromhex(ciphertext_hex)
    ciphertext, tag = data[:-16], data[-16:]
    cipher = AES.new(DETERMINISTIC_ENCRYPTION_KEY, AES.MODE_SIV)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()


# Generate de encryption key 1x (gebruik generate_key.py om deze te genereren)
def generate_key():
    key = Fernet.generate_key()
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        raise Exception(
            "Encryption key niet gevonden: run eerst generate_key().")
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


def verify_password(input_password: str, stored_hash: str) -> bool:
    return hash_password(input_password) == stored_hash


def generate_backup_code() -> str:
    """Generate a one-time backup code."""
    return secrets.token_hex(8)
