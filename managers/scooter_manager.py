from Scooters.Scooters import search_scooter, update_scooter_attributes


def scooter_management_menu(role):
    while True:
        print("\n--- Scooter Management ---")
        print("1. Search Scooter by Serial Number")
        print("2. Update Scooter Info")
        print("3. Back to Main Menu")

        choice = input("Choose option: ").strip()
        if choice == "1":
            search_scooter()
        elif choice == "2":
            update_scooter_attributes(role)
        elif choice == "3":
            break
        else:
            print("Invalid option.")
