from managers.service_engineer_manager import service_engineer_crud
from managers.scooter_manager import scooter_management_menu
from auth.auth_manager import update_own_password


def service_engineer_menu(role):
    while True:
        print("\n--- Service Engineer Menu ---")
        print("1. Manage Scooters")
        print("2. Change Own Password")
        print("3. Logout")
        choice = input("Choose option: ").strip()
        if choice == "1":
            scooter_management_menu(role)
        elif choice == "2":
            update_own_password(role)
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
