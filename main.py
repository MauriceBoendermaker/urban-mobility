from auth.login import Login

from managers.system_admin_manager import system_admin_crud
from managers.service_engineer_manager import service_engineer_crud


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
            print("2. Logout")
            choice = input("Choose option: ").strip()
            if choice == "1":
                service_engineer_crud()
            elif choice == "2":
                print("Logged out.")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
