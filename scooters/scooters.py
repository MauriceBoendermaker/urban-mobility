import sqlite3
from datetime import datetime
from Logging.log_activity import log_activity
from utils.partial_lookup import partial_lookup
from utils.validation import get_valid_input, validate_latitude, validate_longitude, validate_soc_percentage, \
    validate_serial_number, validate_positive_int, validate_iso_date

DB_PATH = "urban_mobility.db"


def add_scooter(session_token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    brand = input("Enter brand: ").strip()
    model = input("Enter model: ").strip()
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
            log_activity(
                session_token, f"Searched for scooter: {scooter['serial_number']}")
    else:
        print("\nScooter not found.")


def update_scooter_attributes(role, session_token):
    if role not in ("service_engineer", "system_admin"):
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

    print("Scooter found. You can update:")
    print("1. Battery %")
    print("2. Location (Lat/Lon)")
    print("3. Service status (out_of_service 0/1)")
    print("4. SOC target min/max")
    choice = input("What do you want to update? ").strip()

    if choice == "1":
        soc = input("New State of Charge (%): ").strip()
        cursor.execute(
            "UPDATE scooters SET soc_percentage=? WHERE serial_number=?", (soc, serial))
    elif choice == "2":
        lat = input("New latitude: ").strip()
        lon = input("New longitude: ").strip()
        cursor.execute("UPDATE scooters SET location_latitude=?, location_longitude=? WHERE serial_number=?",
                       (lat, lon, serial))
    elif choice == "3":
        status = input("Set out_of_service (0 or 1): ").strip()
        cursor.execute(
            "UPDATE scooters SET out_of_service=? WHERE serial_number=?", (status, serial))
    elif choice == "4":
        min_target = input("New SOC min (%): ").strip()
        max_target = input("New SOC max (%): ").strip()
        cursor.execute("UPDATE scooters SET soc_target_min=?, soc_target_max=? WHERE serial_number=?",
                       (min_target, max_target, serial))
    else:
        print("\nInvalid choice.")
        conn.close()
        log_activity(
            session_token, f"Failed to update scooter {serial}",  "Invalid choice")
        return

    conn.commit()
    conn.close()
    print("\nScooter updated.")
    log_activity(
        session_token, f"Updated scooter {serial} attributes: {choice}")
