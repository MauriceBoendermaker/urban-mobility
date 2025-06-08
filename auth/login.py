from utils.encryption import hash_password, deterministic_encrypt, deterministic_decrypt
import sqlite3
import os
from utils.Sessions import create_session, is_session_valid

from utils.encryption import encrypt, hash_password
from datetime import date

# Generate values
username_encrypted = encrypt("super_admin")
first_name_encrypted = encrypt("Super")
last_name_encrypted = encrypt("Admin")
password_hash = hash_password("Admin_123?")
registration_date = str(date.today())

super_admin_user = (
    0,
    username_encrypted,
    password_hash,
    "super_admin",
    first_name_encrypted,
    last_name_encrypted,
    registration_date,
    1
)

super_admin_username = "super_admin"
super_admin_password = "Admin_123?"

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "urban_mobility.db")
DB_PATH = os.path.abspath(DB_PATH)


def Login():
    print("==== Login ====")
    username = input("Username: ")
    password = input("Password: ")

    if username == super_admin_username and password == super_admin_password:
        print("You're logged in as super admin!")
        session_token = create_session(0)
        return (super_admin_user, session_token)
    else:
        # User met username zoeken
        encrypted_username = deterministic_encrypt(username)
        user = get_user(encrypted_username=encrypted_username)
        if user == None:
            print("The username or password is not correct or the account is not active")
            return user
        hashed_password = hash_password(password)
        # (user_id, username_encrypt, password_hash, role, first_name_enc, last_name_enc, registration_date, is_active)
        user_id, password_hash, is_active, first_name_enc, user_role = user[
            0], user[2], user[7], user[4], user[3]
        if hashed_password == password_hash and is_active == 1:
            print(
                f"Welcome, You're logged in as a {user_role}")
            session_token = create_session(user_id)
            return (user, session_token)
        else:
            print("The username or password is not correct or the account is not active")
            return None


def get_user(encrypted_username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM users WHERE username_encrypted = ?""",
        (encrypted_username,))

    user = cursor.fetchall()

    if len(user) < 1:
        return None

    return user[0]
