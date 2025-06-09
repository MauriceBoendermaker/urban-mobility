from utils.encryption import encrypt, decrypt, hash_password, deterministic_encrypt, deterministic_decrypt
from datetime import datetime
import sqlite3
from travellers.Cities import CITIES
from utils.validation import *


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

        choice = input("Choose an option: ").strip()

        if choice == "1":
            travellers = show_all_travellers()
            if travellers == None:
                print("No travellers found!")
            else:
                list_travellers(travellers)

        elif choice == "2":
            register_traveller_menu()
        elif choice == "3":
            update_traveller()
        elif choice == "4":
            delete_traveller()
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def show_all_travellers():
    travellers = cursor.execute("SELECT * FROM travellers").fetchall()

    return travellers if len(travellers) > 0 else None


def register_traveller_menu():

    print("--- register a new traveller ---")

    first_name = get_valid_input(
        "First name: ", validate_name, "First name is not valid")
    last_name = get_valid_input(
        "Last name: ", validate_name, "Last name is not valid")
    birthday = get_valid_input(
        "Birthday (YYYY-MM-DD): ", validate_iso_date, "Birthday format was not valid")
    gender = get_valid_input(
        "Gender (M/F): ", validate_gender, "Invalid input")
    street_name = get_valid_input(
        "Street name: ", validate_street_name, "Invalid street name")
    house_number = get_valid_input(
        "House number: ", validate_house_number, "Invalid house number")
    zip_code = get_valid_input(
        "Zip code: ", validate_zip_code, "Invalid zip code")
    print("Choose the city from the list: ")
    for c in CITIES:
        print(c)
    city_number = get_valid_input(
        f"Enter the number of the city (1-{len(CITIES)}): ", validate_city_number, "Invalid input")

    city = CITIES[int(city_number) - 1].split(" ")[1]

    email_address = get_valid_input(
        "Email address: ", validate_email_address, "Invalid email address")
    mobile_phone = get_valid_input(
        "Mobile phone: ", validate_phone_number, "Invalid phone number")
    driving_license_number = get_valid_input(
        "Driving license number: ", validate_driving_license, "Invalid input")

    register_traveller(
        first_name,
        last_name,
        birthday,
        gender,
        street_name,
        house_number,
        zip_code,
        city,
        email_address,
        mobile_phone,
        driving_license_number
    )


def register_traveller(first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email_address, mobile_phone, driving_license_number):
    try:

        cursor.execute("""
    INSERT INTO travellers (first_name_enc, last_name_enc, birthday, gender, street_name_enc, house_number_enc, zip_code_enc, city, email_enc, mobile_phone_enc, driving_license_enc, registration_date)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
            deterministic_encrypt(first_name),
            deterministic_encrypt(last_name),
            deterministic_encrypt(birthday),
            deterministic_encrypt(gender),
            deterministic_encrypt(street_name),
            deterministic_encrypt(house_number),
            deterministic_encrypt(zip_code),
            deterministic_encrypt(city),
            deterministic_encrypt(email_address),
            deterministic_encrypt(mobile_phone),
            deterministic_encrypt(driving_license_number),
            deterministic_encrypt(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        )
        conn.commit()
        print("System Admin created.")
    except sqlite3.IntegrityError:
        print("Traveller already exists")
    except:
        print("An unexpected error occurred. Please contact support.")
    finally:
        conn.close()


def update_traveller():
    pass


def delete_traveller():
    pass


def list_travellers(travellers):
    pass
