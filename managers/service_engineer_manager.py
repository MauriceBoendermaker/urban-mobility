import sqlite3
from utils.encryption import encrypt, decrypt, hash_password, deterministic_encrypt, deterministic_decrypt
from utils.validation import validate_username, validate_password, validate_name
from datetime import datetime
from travellers.travellers import travellers_crud_menu

DB_PATH = "urban_mobility.db"


def service_engineer_crud():
    while True:
        print("\n--- Service Engineer Management ---")
        print("1. Create Service Engineer")
        print("2. View Service Engineers")
        print("3. Update Service Engineer")
        print("4. Delete Service Engineer")
        print("5. Manage travellers")

        print("6. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_service_engineer()
        elif choice == "2":
            list_service_engineers()
        elif choice == "3":
            update_service_engineer()
        elif choice == "4":
            delete_service_engineer()
        elif choice == "5":
            travellers_crud_menu()
        elif choice == "6":
            break
        else:
            print("Invalid option.")


def create_service_engineer():
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
            encrypt(first_name),
            encrypt(last_name),
            reg_date
        ))
        conn.commit()
        print("Service Engineer created.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()


def list_service_engineers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, username_encrypted, first_name_enc, last_name_enc FROM users WHERE role='service_engineer'")
    rows = cursor.fetchall()

    print("\n--- Service Engineers ---")
    for row in rows:
        user_id, username_enc, fname_enc, lname_enc = row
        print(
            f"[{user_id}] {decrypt(username_enc)} | {decrypt(fname_enc)} {decrypt(lname_enc)}")

    conn.close()


def update_service_engineer():
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
    """, (encrypt(new_fname), encrypt(new_lname), user_id))

    conn.commit()
    conn.close()
    print("Service Engineer updated.")


def delete_service_engineer():
    list_service_engineers()
    user_id = input("Enter Service Engineer ID to delete: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE user_id=? AND role='service_engineer'", (user_id,))
    conn.commit()
    conn.close()
    print("Service Engineer deleted.")
