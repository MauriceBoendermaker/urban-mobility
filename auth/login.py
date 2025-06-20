import os
import sqlite3
import getpass

from datetime import date
from utils.encryption import hash_password, deterministic_encrypt, verify_password, encrypt
from utils.sessions import create_session

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
    cursor.execute(
        "SELECT * FROM users WHERE username_encrypted = ?", (encrypted_username,))
    user = cursor.fetchone()
    conn.close()
    return user


def Login():
    while True:
        print("==== Login ====")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        if username == super_admin_username and password == super_admin_password:
            print("You're logged in as super admin!")
            session_token = create_session(0)
            return (super_admin_user, session_token)
        else:
            # User met username zoeken
            encrypted_username = deterministic_encrypt(username)
            user = get_user(encrypted_username=encrypted_username)
            if user == None:
                print(
                    "The username or password is not correct or the account is not active")
                continue
            # (user_id, username_encrypt, password_hash, role, first_name_enc, last_name_enc, registration_date, is_active)
            user_id, password_hash, is_active, user_role = user[
                0], user[2], user[7], user[3]
            if verify_password(password, password_hash) and is_active == 1:
                print(
                    f"Welcome, You're logged in as a {user_role}")
                session_token = create_session(user_id)
                return (user, session_token)
            else:
                print(
                    "The username or password is not correct or the account is not active")


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
