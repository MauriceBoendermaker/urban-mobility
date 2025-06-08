from utils.encryption import encrypt, decrypt, hash_password, deterministic_encrypt, deterministic_decrypt
from datetime import datetime
import sqlite3
DB_PATH = "urban_mobility.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def travellers_crud_menu():
    while True:
        print("--- travellers management ---")
        print("1. Show all travellers")
        print("2. Register a new traveller")
        print("3. Update traveller")
        print("4. Delete traveller")
        print("5. Go back to the previous menu")

        choice = input("Choose an option").strip()

        if choice == "1":
            break
        elif choice == "2":
            break
        elif choice == "3":
            break
        elif choice == "4":
            break
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def show_all_travellers():
    
    pass


def register_traveller():
    pass


def update_traveller():
    pass


def delete_traveller():
    pass
