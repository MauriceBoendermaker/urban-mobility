import sqlite3
import os
from src.utils.encryption import hash_password
from src.utils.validation import validate_password

DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db")


def update_own_password(user_id):

    while True:
        new_password = input("Enter new password: ").strip()
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
    delete = False
    while True:
        confirm = input(
            "Are you sure you want to delete your own account (y/n)? ").upper()
        if confirm == "Y":
            delete = True
            break
        if confirm == "N":
            delete = False
            break

    if delete:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=?",
                       (user_id, ))
        conn.commit()
        conn.close()
        return True
    else:
        return False
