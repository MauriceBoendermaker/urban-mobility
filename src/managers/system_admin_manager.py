import os
import sqlite3

from datetime import datetime
from src.activity_logs.log_activity import log_activity
from src.utils.validation import validate_username, validate_password, validate_name
from src.utils.encryption import encrypt, decrypt, hash_password, deterministic_encrypt, deterministic_decrypt


DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db")


def system_admin_crud(session_token):
    while True:
        print("\n--- System Admin Management ---")
        print("1. Create System Admin")
        print("2. View System Admins")
        print("3. Update System Admin")
        print("4. Delete System Admin")

        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_system_admin(session_token)
        elif choice == "2":
            list_system_admins(session_token)
        elif choice == "3":
            update_system_admin(session_token)
        elif choice == "4":
            delete_system_admin(session_token)

        elif choice == "5":
            break
        else:
            print("Invalid option.")


def create_system_admin(session_token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        username = input("Enter username (8–10 chars): ").strip()
        valid, errors = validate_username(username)
        if not valid:
            print("Username is invalid:")
            for error in errors:
                print(" -", error)
        else:
            break

    while True:
        password = input("Enter password: ").strip()
        valid, errors = validate_password(password)
        if not valid:
            print("Password does not meet requirements:")
            for error in errors:
                print(" -", error)
        else:
            break

    while True:
        first_name = input("First name: ").strip()
        valid, errors = validate_name(first_name)
        if not valid:
            print("Invalid first name:")
            for error in errors:
                print(" -", error)
        else:
            break

    while True:
        last_name = input("Last name: ").strip()
        valid, errors = validate_name(last_name)
        if not valid:
            print("Invalid last name:")
            for error in errors:
                print(" -", error)
        else:
            break

    reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO users (username_encrypted, password_hash, role, first_name_enc, last_name_enc, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            deterministic_encrypt(username),
            hash_password(password),
            "system_admin",
            encrypt(first_name),
            encrypt(last_name),
            reg_date
        ))
        conn.commit()
        print("System Admin created.")
        log_activity(session_token, f"Created System Admin: {username}")
    except sqlite3.IntegrityError:
        print("Username already exists.")
        log_activity(
            session_token, f"Failed to create System Admin: {username}", "(username exists)")
    except Exception as e:
        print("An error occurred while creating System Admin:")
        log_activity(
            session_token, f"Error creating System Admin: {username}", str(e))
    finally:
        conn.close()


def list_system_admins(session_token=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, username_encrypted, first_name_enc, last_name_enc FROM users WHERE role='system_admin'")
    rows = cursor.fetchall()

    print("\n--- System Admins ---")
    for row in rows:
        user_id, username_enc, fname_enc, lname_enc = row
        print(
            f"[{user_id}] {deterministic_decrypt(username_enc)} | {decrypt(fname_enc)} {decrypt(lname_enc)}")
        if session_token:
            log_activity(session_token, "Listed System Admins")
    conn.close()
    return rows


def update_system_admin(session_token):
    user_id = input("Enter System Admin ID to update: ").strip()

    while True:
        new_fname = input("New first name: ").strip()
        valid, errors = validate_name(new_fname)
        if not valid:
            print("Invalid first name:")
            for error in errors:
                print(" -", error)
        else:
            break

    while True:
        new_lname = input("New last name: ").strip()
        valid, errors = validate_name(new_lname)
        if not valid:
            print("Invalid last name:")
            for error in errors:
                print(" -", error)
        else:
            break

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET first_name_enc=?, last_name_enc=?
        WHERE user_id=? AND role='system_admin'
    """, (encrypt(new_fname), encrypt(new_lname), user_id))

    conn.commit()
    conn.close()
    print("System Admin updated.")
    log_activity(session_token, f"Updated System Admin ID: {user_id}")


def delete_system_admin(session_token):
    list_system_admins()
    user_id = input("Enter System Admin ID to delete: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE user_id=? AND role='system_admin'", (user_id,))
    conn.commit()
    conn.close()
    print("System Admin deleted.")
    log_activity(session_token, f"Deleted System Admin ID: {user_id}")
