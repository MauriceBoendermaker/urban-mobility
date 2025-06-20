import os
import sqlite3

from src.utils.validation import *
from src.activity_logs.log_activity import log_activity
from src.utils.encryption import deterministic_encrypt, deterministic_decrypt

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db"))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def travellers_crud_menu(session_token):
    while True:
        print("\n--- Travellers Management ---")
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
                log_activity(session_token, "Listed all travellers")
        elif choice == "2":
            register_traveller_menu(session_token)
        elif choice == "3":
            travellers = show_all_travellers()
            if travellers == None:
                print("\nNo travellers found!")
            else:
                update_travellers_menu(travellers, session_token)
        elif choice == "4":
            travellers = show_all_travellers()
            if travellers == None:
                print("\nNo travellers found!")
            else:
                delete_traveller_menu(travellers, session_token)
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def show_all_travellers():
    travellers = cursor.execute(
        "SELECT * FROM travellers").fetchall()

    return travellers if len(travellers) > 0 else None


def register_traveller_menu(session_token):
    print("\n--- Register a new traveller ---")

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
        "Mobile phone: +31 6", validate_phone_number, "Invalid phone number")
    driving_license_number = get_valid_input(
        "Driving license number: ", validate_driving_license, "Invalid input")

    mobile_phone = "+31 6" + mobile_phone

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
        driving_license_number, session_token
    )


def register_traveller(first_name, last_name, birthday, gender, street_name, house_number, zip_code, city,
                       email_address, mobile_phone, driving_license_number, session_token):
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
        print("Traveller created.")
        log_activity(
            session_token, f"Registered new traveller: {first_name} {last_name}")
    except sqlite3.IntegrityError:
        print("Traveller already exists")
        log_activity(session_token, "Failed to register traveller",
                     "Duplicate entry")
    except Exception as e:
        print("An unexpected error occurred. Please contact support.")
        log_activity(session_token, "Failed to register traveller",
                     "Unexpected error: " + str(e))


def update_travellers_menu(travellers, session_token):
    list_travellers(travellers)
    traveller_id = -1
    while True:
        input_id = input(
            "Enter the ID of the traveller you want to update: ").strip()
        try:
            traveller_id = int(input_id)
            id_exists = False
            for traveller in travellers:
                if traveller[0] == traveller_id:
                    id_exists = True

            if not id_exists:
                print(f"The traveller with id {traveller_id} doesn't exist")
            else:
                break
        except:
            print("Invalid input")

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
        "Zip code: ", validate_zip_code, "Invalid zip code", True)
    print("Choose the city from the list: ")
    for c in CITIES:
        print(c)
    city_number = get_valid_input(
        f"Enter the number of the city (1-{len(CITIES)}): ", validate_city_number, "Invalid input")

    city = CITIES[int(city_number) - 1].split(" ")[1]

    email_address = get_valid_input(
        "Email address: ", validate_email_address, "Invalid email address")
    mobile_phone = get_valid_input(
        "Mobile phone: +31 6", validate_phone_number, "Invalid phone number")
    driving_license_number = get_valid_input(
        "Driving license number: ", validate_driving_license, "Invalid input", True)

    mobile_phone = "+31 6" + mobile_phone

    update_traveller(
        traveller_id,
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
        driving_license_number, session_token
    )


def update_traveller(id, first_name, last_name, birthday, gender, street_name, house_number, zip_code, city,
                     email_address, mobile_phone, driving_license_number, session_token):
    try:
        cursor.execute("""
            UPDATE travellers
            SET first_name_enc=?, last_name_enc=?, birthday=?, gender=?, street_name_enc=?, house_number_enc=?, zip_code_enc=?, city=?, email_enc=?, mobile_phone_enc=?, driving_license_enc=?
            WHERE traveller_id=?
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
            id
        ))
        conn.commit()
        print("Traveller updated successfully.")
        log_activity(session_token, f"Updated traveller ID: {id}")
    except Exception as e:
        print("An error occurred while updating the traveller:", e)
        log_activity(
            session_token, f"Failed to update traveller ID: {id}", str(e))


def delete_traveller_menu(travellers, session_token):
    list_travellers(travellers)
    traveller_id = -1
    while True:
        input_id = input(
            "Enter the ID of the traveller you want to update: ").strip()
        try:
            traveller_id = int(input_id)
            id_exists = False
            for traveller in travellers:
                if traveller[0] == traveller_id:
                    id_exists = True

            if not id_exists:
                print(f"The traveller with id {traveller_id} doesn't exist")
            else:
                break
        except:
            print("Invalid input")
    delete_traveller(traveller_id, session_token)


def delete_traveller(id, session_token):
    try:

        cursor.execute("""DELETE FROM travellers WHERE traveller_id = ?;
        """, str(id))
        print("traveller with id {id} has been succesfully deleted")
        log_activity(
            session_token, f"Deleted traveller ID: {id}")
    except Exception as e:
        print(
            f"An error has occured while deleting traveller with id :{id}", e)
        log_activity(
            session_token, f"Failed to delete traveller ID: {id}", str(e))


def list_travellers(travellers):
    print("--- Travellers ---")

    for t in travellers:
        traveller_id, first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email_address, mobile_phone, driving_license_number, registration_date = t
        print(
            f"""ID: {traveller_id}, Full name: {deterministic_decrypt(first_name)} {deterministic_decrypt(last_name)}, """
            f"""Birthday: {deterministic_decrypt(birthday)}, Gender: {"Male" if deterministic_decrypt(gender).upper() else "Female"}, """
            f"""Address: {deterministic_decrypt(street_name)} {deterministic_decrypt(house_number)}, {deterministic_decrypt(zip_code)} {deterministic_decrypt(city)}, """
            f"""Email: {deterministic_decrypt(email_address)}, Phone: {deterministic_decrypt(mobile_phone)}, """
            f"""Driving License: {deterministic_decrypt(driving_license_number)}, Registered since: {deterministic_decrypt(registration_date)}\n"""
        )
