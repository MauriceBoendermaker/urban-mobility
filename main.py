# from auth.login import login
from managers.system_admin_manager import system_admin_crud
from auth.login import Login
from Scooters import scooters_menu


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
            print("1. Manage Scooters")
            print("2. Manage account")
            print("3. Manage users")
            print("4. Manage Backups")
            print("5. Manage travellers")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                # Scooters GET
                scooters_menu(user)
            elif choice == "2":
                # Account deletion, Password reset
                Accounts

            elif choice == "3":
                # Service Engineers CRUD &
                pass
            elif choice == "4":
                # backup
                pass

            elif choice == "5":
                # Travellers CRUD
                pass

            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
