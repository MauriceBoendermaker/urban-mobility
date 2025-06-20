import sqlite3

from datetime import datetime
from activity_logs.log_activity import log_activity
from utils.validation import validate_username, validate_password, validate_name
from utils.encryption import hash_password, deterministic_encrypt, deterministic_decrypt

DB_PATH = "urban_mobility.db"


def service_engineer_crud(session_token):
    while True:
        print("\n--- Service Engineer Management ---")
        print("1. Create Service Engineer")
        print("2. View Service Engineers")
        print("3. Update Service Engineer")
        print("4. Delete Service Engineer")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_service_engineer(session_token)
        elif choice == "2":
            list_service_engineers(session_token)
        elif choice == "3":
            update_service_engineer(session_token)
        elif choice == "4":
            delete_service_engineer(session_token)
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def create_service_engineer(session_token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        username = input("Enter username (8-10 chars): ").strip()
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
            "service_engineer",
            deterministic_encrypt(first_name),
            deterministic_encrypt(last_name),
            reg_date
        ))
        conn.commit()
        print("Service Engineer created.")
        log_activity(session_token, f"Created Service Engineer: {username}")
    except sqlite3.IntegrityError:
        print("Username already exists.")
        log_activity(
            session_token, f"Failed to create Service Engineer: {username} (Username exists)")
    except Exception as e:
        print(f"Error creating Service Engineer")
        log_activity(
            session_token, f"Error creating Service Engineer: {username}", str(e))
    finally:
        conn.close()


def list_service_engineers(session_token=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, username_encrypted, first_name_enc, last_name_enc FROM users WHERE role='service_engineer'")
    rows = cursor.fetchall()

    print("\n--- Service Engineers ---")
    try:

        for row in rows:
            user_id, username_enc, fname_enc, lname_enc = row
            print(
                f"[{user_id}] {deterministic_decrypt(username_enc)} | {deterministic_decrypt(fname_enc)} {deterministic_decrypt(lname_enc)}")
            if session_token:
                log_activity(
                    session_token, f"Viewed Service Engineer: {deterministic_decrypt(username_enc)}")
    except Exception as e:
        print("Error retrieving service engineers")
        log_activity(session_token, "Error listing Service Engineers", str(e))
    finally:
        conn.close()


def update_service_engineer(session_token):
    list_service_engineers()
    user_id = input("Enter Service Engineer ID to update: ").strip()

    new_fname = input("New first name: ").strip()
    new_lname = input("New last name: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET first_name_enc=?, last_name_enc=?
        WHERE user_id=? AND role='service_engineer'
    """, (deterministic_encrypt(new_fname), deterministic_encrypt(new_lname), user_id))

    conn.commit()
    conn.close()
    print("Service Engineer updated.")
    log_activity(session_token, f"Updated Service Engineer ID: {user_id}")


def delete_service_engineer(session_token):
    list_service_engineers()
    user_id = input("Enter Service Engineer ID to delete: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE user_id=? AND role='service_engineer'", (user_id,))
    conn.commit()
    conn.close()
    print("Service Engineer deleted.")
    log_activity(session_token, f"Deleted Service Engineer ID: {user_id}")
