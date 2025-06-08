from managers.system_admin_manager import system_admin_crud


def super_admin_menu():
    while True:
        print("\n--- Super Admin Menu ---")
        print("1. Manage System Administrators")
        print("2. View Logs (komt binnenkort)")
        print("3. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            system_admin_crud()
            break
        elif choice == "2":
            print("Logs komt hierna.")
            break
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
