import sqlite3
from datetime import datetime
from utils.validation import get_valid_input, validate_latitude, validate_longitude, validate_soc_percentage

DB_PATH = "urban_mobility.db"


def add_scooter():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    brand = input("Enter brand: ").strip()
    model = input("Enter model: ").strip()
    serial = input("Enter serial number (10–17 chars): ").strip()

    top_speed = int(input("Enter top speed (km/h): "))
    battery_capacity = int(input("Enter battery capacity (Wh): "))
    soc = int(get_valid_input("Enter SoC (%): ", validate_soc_percentage, "Invalid SoC"))
    soc_min = int(get_valid_input("Enter SoC target min: ", validate_soc_percentage, "Invalid min SoC"))
    soc_max = int(get_valid_input("Enter SoC target max: ", validate_soc_percentage, "Invalid max SoC"))
    lat = float(get_valid_input("Enter latitude: ", validate_latitude, "Invalid latitude"))
    lon = float(get_valid_input("Enter longitude: ", validate_longitude, "Invalid longitude"))
    mileage = int(input("Enter mileage (km): "))
    maintenance_date = input("Enter last maintenance date (YYYY-MM-DD): ").strip()
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
    print("\nScooter added.")


def delete_scooter():
    serial = input("Enter serial number to delete: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scooters WHERE serial_number = ?", (serial,))
    conn.commit()
    conn.close()
    print("\nScooter deleted.")


def list_all_scooters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters")
    scooters = cursor.fetchall()
    conn.close()

    if scooters:
        for s in scooters:
            print(s)
    else:
        print("\nNo scooters found.")


def search_scooter():
    serial = input("Enter scooter serial number: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters WHERE serial_number = ?", (serial,))
    scooter = cursor.fetchone()

    if scooter:
        print("\nScooter found:")
        print(scooter)
    else:
        print("\nScooter not found.")
    conn.close()


def update_scooter_attributes(role):
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
        cursor.execute("UPDATE scooters SET soc_percentage=? WHERE serial_number=?", (soc, serial))
    elif choice == "2":
        lat = input("New latitude: ").strip()
        lon = input("New longitude: ").strip()
        cursor.execute("UPDATE scooters SET location_latitude=?, location_longitude=? WHERE serial_number=?",
                       (lat, lon, serial))
    elif choice == "3":
        status = input("Set out_of_service (0 or 1): ").strip()
        cursor.execute("UPDATE scooters SET out_of_service=? WHERE serial_number=?", (status, serial))
    elif choice == "4":
        min_target = input("New SOC min (%): ").strip()
        max_target = input("New SOC max (%): ").strip()
        cursor.execute("UPDATE scooters SET soc_target_min=?, soc_target_max=? WHERE serial_number=?",
                       (min_target, max_target, serial))
    else:
        print("\nInvalid choice.")
        conn.close()
        return

    conn.commit()
    conn.close()
    print("\nScooter updated.")
