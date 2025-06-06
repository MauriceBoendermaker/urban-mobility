import sqlite3
from utils.encryption import hash_password
from utils.validation import validate_password

DB_PATH = "urban_mobility.db"


def update_own_password(user):
    user_id = user[0]

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
    cursor.execute("UPDATE users SET password_hash=? WHERE user_id=?", (hash_password(new_password), user_id))
    conn.commit()
    conn.close()

    print("Password updated successfully.")
