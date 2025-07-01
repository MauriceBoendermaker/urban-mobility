import os
import sqlite3

from datetime import datetime
from src.utils.partial_lookup import partial_lookup
from src.activity_logs.log_activity import log_activity
from src.utils.validation import get_valid_input, validate_latitude, validate_longitude, validate_soc_percentage, \
    validate_serial_number, validate_positive_int, validate_iso_date, validate_brand, validate_model

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "urban_mobility.db"))


def add_scooter(session_token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    brand = get_valid_input("Enter brand: ", validate_brand, "Invalid brand")
    model = get_valid_input("Enter model: ", validate_model, "Invalid model")
    serial = get_valid_input("Enter serial number (10–17 chars): ",
                             validate_serial_number, "Invalid serial number")

    top_speed = int(get_valid_input("Enter top speed (km/h): ",
                                    validate_positive_int, "Invalid top speed"))
    battery_capacity = int(
        get_valid_input("Enter battery capacity (Wh): ", validate_positive_int, "Invalid battery capacity"))
    soc = int(get_valid_input("Enter SoC (%): ",
                              validate_soc_percentage, "Invalid SoC"))
    soc_min = int(get_valid_input("Enter SoC target min: ",
                                  validate_soc_percentage, "Invalid min SoC"))
    soc_max = int(get_valid_input("Enter SoC target max: ",
                                  validate_soc_percentage, "Invalid max SoC"))
    lat = float(get_valid_input("Enter latitude: ",
                                validate_latitude, "Invalid latitude"))
    lon = float(get_valid_input("Enter longitude: ",
                                validate_longitude, "Invalid longitude"))
    mileage = int(get_valid_input("Enter mileage (km): ",
                                  validate_positive_int, "Invalid mileage"))
    maintenance_date = get_valid_input(
        "Enter last maintenance date (YYYY-MM-DD): ", validate_iso_date, "Invalid date")
    in_service_date = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO scooters (
            brand, model, serial_number, top_speed, battery_capacity, soc_percentage,
            soc_target_min, soc_target_max, location_latitude, location_longitude,
            out_of_service, mileage_km, last_maintenance, in_service_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
    """, (brand, model, serial, top_speed, battery_capacity, soc,
          soc_min, soc_max, lat, lon, mileage, maintenance_date, in_service_date))

    conn.commit()
    conn.close()
    log_activity(session_token, f"Added scooter: {serial}", additional_info={
        "brand": brand,
        "model": model,
        "top_speed": top_speed,
        "battery_capacity": battery_capacity,
        "soc": soc,
        "location": (lat, lon),
        "mileage": mileage,
        "last_maintenance": maintenance_date
    })
    print("\nScooter added.")


def delete_scooter(session_token):
    serial = input("Enter serial number to delete: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scooters WHERE serial_number = ?", (serial,))
    conn.commit()
    conn.close()
    print("\nScooter deleted.")
    log_activity(session_token, f"Deleted scooter: {serial}")


def list_all_scooters(session_token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters")
    scooters = cursor.fetchall()
    conn.close()

    if scooters:
        for s in scooters:
            print(s)
        log_activity(session_token, "Listed all scooters")
    else:
        print("\nNo scooters found.")
        log_activity(
            session_token, "Tried to list all scooters but none found")


def search_scooter(session_token):
    partial = input("Enter scooter serial number (partial is fine): ").strip()

    results = partial_lookup("scooters", "serial_number", partial)

    if results:
        print(f"\nFound {len(results)} scooter(s):\n")
        for scooter in results:
            print(scooter)
            log_activity(session_token, f"Searched for scooter: {scooter[3]}")
    else:
        print("\nScooter not found.")


def update_scooter_attributes(role, session_token):
    if role not in ("service_engineer", "system_admin", "super_admin"):
        print("You do not have permission to update scooter data.")
        return

    serial = input("Enter scooter serial number: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scooters WHERE serial_number = ?", (serial,))
    scooter = cursor.fetchone()
    if not scooter:
        print("\nScooter not found.")
        conn.close()
        return

    print("\nScooter found. You can update:")

    editable_options = []

    if role in ("system_admin", "super_admin", "service_engineer"):
        editable_options += [
            ("1", "Battery %"),
            ("2", "Location (Lat/Lon)"),
            ("3", "Out-of-service status"),
            ("4", "SOC target min/max"),
            ("5", "Mileage"),
            ("6", "Last maintenance date")
        ]

    for opt in editable_options:
        print(f"{opt[0]}. {opt[1]}")

    choice = input("What do you want to update?")
    if choice is None:
        print("Returning to login screen...\n")
        return
    choice = choice.strip()

    try:
        if choice == "1":
            soc = int(input("New State of Charge (%): ").strip())
            cursor.execute("UPDATE scooters SET soc_percentage=? WHERE serial_number=?", (soc, serial))

        elif choice == "2":
            lat = float(input("New latitude: ").strip())
            lon = float(input("New longitude: ").strip())
            if not validate_latitude(lat) or not validate_longitude(lon):
                print("Invalid coordinates. Must be within Rotterdam.")
                return
            cursor.execute("UPDATE scooters SET location_latitude=?, location_longitude=? WHERE serial_number=?",
                           (lat, lon, serial))

        elif choice == "3":
            status = int(input("Set out_of_service (0 or 1): ").strip())
            if status not in (0, 1):
                print("Invalid value. Must be 0 or 1.")
                return
            cursor.execute("UPDATE scooters SET out_of_service=? WHERE serial_number=?", (status, serial))

        elif choice == "4":
            min_target = int(input("New SOC target min (%): ").strip())
            max_target = int(input("New SOC target max (%): ").strip())
            cursor.execute("UPDATE scooters SET soc_target_min=?, soc_target_max=? WHERE serial_number=?",
                           (min_target, max_target, serial))

        elif choice == "5":
            mileage = int(input("New mileage (km): ").strip())
            cursor.execute("UPDATE scooters SET mileage_km=? WHERE serial_number=?", (mileage, serial))

        elif choice == "6":
            date_str = input("New maintenance date (YYYY-MM-DD): ").strip()
            if not validate_iso_date(date_str):
                print("Invalid date format. Use YYYY-MM-DD.")
                return
            cursor.execute("UPDATE scooters SET last_maintenance=? WHERE serial_number=?", (date_str, serial))

        else:
            print("\nInvalid choice.")
            log_activity(session_token, f"Failed to update scooter {serial}", "Invalid update option")
            return

        conn.commit()
        print("\nScooter updated successfully.")
        log_activity(session_token, f"Updated scooter {serial}", f"Field: {choice}")

    except Exception as e:
        print(f"Error updating scooter: {e}")
        log_activity(session_token, f"Exception while updating scooter {serial}", str(e))

    finally:
        conn.close()
