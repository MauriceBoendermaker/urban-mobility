from managers.system_admin_manager import system_admin_crud
from travellers.travellers import travellers_crud_menu
from backup_manager import create_backup, restore_backup


def super_admin_menu():
    while True:
        print("\n--- Super Admin Menu ---")
        print("1. Manage System Administrators")
        print("2. View Logs (komt binnenkort)")
        print("3. Manage travellers")
        print("4. Create Backup")
        print("5. Restore Backup")
        print("6. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            system_admin_crud()
            break
        elif choice == "2":
            print("Logs komt hierna.")
            break
        elif choice == "3":
            travellers_crud_menu()
            break

        elif choice == "4":
            create_backup()
            break
        elif choice == "5":
            backup_file = input("Enter the backup file name to restore: ").strip()
            restore_backup(backup_file)
            break
        else:
            print("Invalid choice.")
