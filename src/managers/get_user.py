import os
import sqlite3

from src.auth.login import super_admin_user
from src.utils.encryption import deterministic_decrypt, decrypt

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db"))


def get_user(user_id):
    if user_id == 0:
        return {
            "user_id": 0,
            "username": "super_admin",
            "role": "super_admin",
            "first_name": "Super",
            "last_name": "Admin",
            "registration_date": super_admin_user[6],
            "is_active": 1
        }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("User not found.")
        return None

    return {
        "user_id": row[0],
        "username": deterministic_decrypt(row[1]),
        "role": row[3],
        "first_name": decrypt(row[4]),
        "last_name": decrypt(row[5]),
        "registration_date": row[6],
        "is_active": row[7]
    }
