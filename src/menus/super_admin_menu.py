from src.activity_logs.read_log import read_log
from src.activity_logs.log_activity import log_activity
from src.managers.system_admin_manager import system_admin_crud
from src.managers.travellers_manager import travellers_crud_menu
from src.managers.scooter_manager import scooter_management_menu
from src.managers.service_engineer_manager import service_engineer_crud
from src.utils.backup_manager import Revoke_Backup, create_backup, restore_backup, assign_backup_to_system_admin


def super_admin_menu(session_token):
    while True:
        print("\n--- Super Admin Menu ---")
        print("1. Manage System Administrators")
        print("2. Manage Service Engineers")
        print("3. Manage Travellers")
        print("4. Manage Scooters")
        print("5. Manage Backups")
        print("6. View Logs")
        print("7. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            system_admin_crud(session_token)
        if choice == "2":
            service_engineer_crud(session_token)
        elif choice == "3":
            travellers_crud_menu(session_token)
        elif choice == "4":
            scooter_management_menu(session_token)
        elif choice == "5":
            manage_backups(session_token)
        elif choice == "6":
            read_log()
            log_activity(session_token, "Viewed Logs")
        elif choice == "7":
            print("activity_logs out.")
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
