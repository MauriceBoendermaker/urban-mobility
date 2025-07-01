import os
import sqlite3

from src.utils.encryption import hash_password
from src.utils.validation import validate_password
from src.utils.password_helper import input_password

DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db")


def update_own_password(user_id):
    while True:
        new_password = input_password("Enter password: ")
        if new_password is None:
            print("Password change cancelled.")
            return
        new_password = new_password.strip()

        valid, errors = validate_password(new_password)
        if not valid:
            print("Password is invalid:")
            for error in errors:
                print(" -", error)
        else:
            break

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash=? WHERE user_id=?",
                   (hash_password(new_password), user_id))
    conn.commit()
    conn.close()

    print("Password updated successfully.")


def delete_own_account(user_id):
    while True:
        confirm = input("Are you sure you want to delete your own account (y/n)? ")
        if confirm is None:
            print("Cancelled.")
            return False

        confirm = confirm.upper()
        if confirm == "Y":
            break
        elif confirm == "N":
            return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return True
