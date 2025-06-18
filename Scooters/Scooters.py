import sqlite3

DB_PATH = "urban_mobility.db"


def search_scooter():
    serial = input("Enter scooter serial number: ").strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scooters WHERE serial_number = ?", (serial,))
    scooter = cursor.fetchone()
    if scooter:
        print("Scooter found:")
        print(scooter)
    else:
        print("Scooter not found.")
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
        print("Scooter not found.")
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
        print("Invalid choice.")
        conn.close()
        return

    conn.commit()
    conn.close()
    print("Scooter updated.")
