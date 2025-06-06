from auth.login import Login
from auth.auth_manager import update_own_password

from managers.system_admin_manager import system_admin_crud
from managers.service_engineer_manager import service_engineer_crud
from managers.scooter_manager import scooter_management_menu


def main():
    user = None
    while not user:
        user = Login()

    while True:
        if user[3] == "super_admin":
            print("\n--- Super Admin Menu ---")
            print("1. Manage System Administrators")
            print("2. View Logs (komt binnenkort)")
            print("3. Logout")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                system_admin_crud()
            elif choice == "2":
                print("Logs komt hierna.")
            elif choice == "3":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

        elif user[3] == "system_admin":
            print("\n--- System Admin Menu ---")
            print("1. Manage Service Engineers")
            print("2. Manage Scooters")
            print("3. Change Own Password")
            print("4. Logout")
            choice = input("Choose option: ").strip()
            if choice == "1":
                service_engineer_crud()
            elif choice == "2":
                scooter_management_menu(user[3])
            elif choice == "3":
                update_own_password(user)
            elif choice == "4":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")

        elif user[3] == "service_engineer":
            print("\n--- Service Engineer Menu ---")
            print("1. Manage Scooters")
            print("2. Change Own Password")
            print("3. Logout")
            choice = input("Choose option: ").strip()
            if choice == "1":
                scooter_management_menu(user[3])
            elif choice == "2":
                update_own_password(user)
            elif choice == "3":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
