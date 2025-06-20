from managers.system_admin_manager import system_admin_crud
from managers.travellers_manager import travellers_crud_menu
from utils.backup_manager import Revoke_Backup, create_backup, restore_backup, assign_backup_to_system_admin
from Logging.Read_log import read_log


def super_admin_menu(session_token):
    while True:
        print("\n--- Super Admin Menu ---")
        print("1. Manage System Administrators")
        print("2. View Logs")
        print("3. Manage Travellers")
        print("4. Manage Backups")
        print("5. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            system_admin_crud()
        elif choice == "2":
            read_log()
        elif choice == "3":
            travellers_crud_menu()
        elif choice == "4":
            manage_backups(session_token)
        elif choice == "5":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")


def manage_backups(session_token):
    while True:
        print("\n--- Manage Backups ---")
        print("1. Create Backup")
        print("2. Restore Backup")
        print("3. Assign Backup to System Admin")
        print("4. Revoke Backup")
        print("5. Back to Super Admin Menu")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            create_backup(session_token)
        elif choice == "2":
            restore_backup(session_token)
        elif choice == "3":
            assign_backup_to_system_admin(session_token=session_token)
        elif choice == "4":

            Revoke_Backup()
        elif choice == "5":
            print("Returning to Super Admin Menu.")
            break
        else:
            print("Invalid choice.")
