from utils.encryption import hash_password, deterministic_encrypt, verify_password, encrypt, decrypt
import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "urban_mobility.db")
DB_PATH = os.path.abspath(DB_PATH)

super_admin_username = "super_admin"
super_admin_password = "Admin_123?"

super_admin_user = (
    0,
    deterministic_encrypt(super_admin_username),
    hash_password(super_admin_password),
    "super_admin",
    encrypt("Super"),
    encrypt("Admin"),
    str(date.today()),
    1
)


def get_user(encrypted_username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username_encrypted = ?", (encrypted_username,))
    user = cursor.fetchone()
    conn.close()
    return user


def Login():
    print("==== Login ====")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username == super_admin_username and password == super_admin_password:
        print("You're logged in as super admin!")
        return super_admin_user

    encrypted_username = deterministic_encrypt(username)
    user = get_user(encrypted_username)

    if user is None:
        print("The username or password is not correct or the account is not active")
        return None

    stored_hash = user[2]
    is_active = user[7]
    first_name = decrypt(user[4])
    role = user[3]

    if verify_password(password, stored_hash) and is_active == 1:
        print(f"Welcome {first_name}! You're logged in as {role}.")
        return user
    else:
        print("The username or password is not correct or the account is not active")
        return None
