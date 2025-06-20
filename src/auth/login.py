import os
import sqlite3
import getpass

from datetime import date
from src.utils.sessions import create_session
from src.utils.encryption import hash_password, deterministic_encrypt, verify_password, encrypt
from src.utils.validation import validate_sql_injection_attempt

DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db")
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

MAX_ATTEMPTS = 3
login_attempts = {}


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
        suspicious_activity = None
        print("==== Login ====")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        login_attempts[username] = login_attempts.get(username, 0)

        if validate_sql_injection_attempt(username) or validate_sql_injection_attempt(password):
            suspicious_activity = [username, password,
                                   "Possible SQL injection attempt", True]

        if username == super_admin_username and password == super_admin_password:
            print("You're logged in as super admin!")
            session_token = create_session(0)
            login_attempts[username] = 0  # reset on success
            return (super_admin_user, session_token, suspicious_activity)
        else:
            encrypted_username = deterministic_encrypt(username)
            user = get_user(encrypted_username=encrypted_username)

            if user is None:
                print(
                    "The username or password is not correct or the account is not active")
                login_attempts[username] += 1
            else:
                user_id, password_hash, is_active, user_role = user[0], user[2], user[7], user[3]
                if verify_password(password, password_hash) and is_active == 1:
                    print(f"Welcome, You're logged in as a {user_role}")
                    session_token = create_session(user_id)
                    login_attempts[username] = 0  # reset on success
                    return (user, session_token, suspicious_activity)
                else:
                    print(
                        "The username or password is not correct or the account is not active")
                    login_attempts[username] += 1

        if login_attempts[username] >= MAX_ATTEMPTS:
            print(f"Too many failed attempts for '{username}'")
            suspicious_activity = [username, password,
                                   f"{MAX_ATTEMPTS} failed login attempts", True]
            login_attempts[username] = 0
            return (None, None, suspicious_activity)


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
