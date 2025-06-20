import sqlite3
from utils.encryption import deterministic_decrypt
DB_PATH = "urban_mobility.db"


def get_user(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?", (id,))
    row = cursor.fetchone()

    conn.close()
    if row:
        return {
            "username": deterministic_decrypt(row[1]),
            "role": row[3],
        }
    else:
        print("User not found.")
        return None
