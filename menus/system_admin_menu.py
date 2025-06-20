from managers.service_engineer_manager import service_engineer_crud
from utils.backup_manager import create_backup


def system_admin_menu(session_token):
    while True:

        print("\n--- System Admin Menu ---")
        print("1. Manage Service Engineers")
        print("2. Manage travellers")
        print("3. Create Backup")
        print("4. Logout")
        choice = input("Choose option: ").strip()
        if choice == "1":
            service_engineer_crud()
        elif choice == "2":
            print("Logged out.")
            break
        elif choice == "3":
            create_backup(session_token)
        elif choice == "4":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")
