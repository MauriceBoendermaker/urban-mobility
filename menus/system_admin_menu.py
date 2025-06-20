from managers.service_engineer_manager import service_engineer_crud
from utils.backup_manager import create_backup, restore_backup
from managers.travellers_manager import travellers_crud_menu


def system_admin_menu(session_token):
    while True:
        print("\n--- System Admin Menu ---")
        print("1. Manage Service Engineers")
        print("2. Manage Travellers")
        print("3. Create Backup")
        print("4. Restore Backup")
        print("5. View Logs (komt binnenkort)")
        print("6. Logout")
        choice = input("Choose option: ").strip()

        if choice == "1":
            service_engineer_crud()
        elif choice == "2":
            travellers_crud_menu()
        elif choice == "3":
            create_backup(session_token)
        elif choice == "4":
            restore_backup(session_token)
        elif choice == "5":
            print("Viewing logs...")
        elif choice == "6":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")
