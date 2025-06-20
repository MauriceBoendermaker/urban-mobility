from Scooters.Scooters import add_scooter, delete_scooter, update_scooter_attributes, search_scooter, list_all_scooters
from auth.login import get_user


def scooter_management_menu(role):
    while True:
        print("\n--- Scooter Management ---")
        print("1. Search scooter")
        print("2. Update scooter")
        if role != "service_engineer":
            print("3. Add new scooter")
            print("4. Delete scooter")
        print("5. List all scooters")
        print("6. Back")

        choice = input("Choose option: ").strip()

        if choice == "1":
            search_scooter()
        elif choice == "2":
            update_scooter_attributes(role)
        elif choice == "3" and role != "service_engineer":
            add_scooter()
        elif choice == "4" and role != "service_engineer":
            delete_scooter()
        elif choice == "5":
            list_all_scooters()
        elif choice == "6":
            break
        else:
            print("Invalid choice or insufficient permissions.")
