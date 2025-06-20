from Logging.log_activity import log_activity
from managers.service_engineer_manager import service_engineer_crud
from utils.backup_manager import create_backup, restore_backup
from managers.travellers_manager import travellers_crud_menu
from managers.scooter_manager import scooter_management_menu
from Logging.Read_log import read_log


def system_admin_menu(session_token):
    while True:
        print("\n--- System Admin Menu ---")
        print("1. Manage Service Engineers")
        print("2. Manage Travellers")
        print("3. Manage Scooters")
        print("4. Create Backup")
        print("5. Restore Backup")
        print("6. View Logs")
        print("7. Logout")
        choice = input("Choose option: ").strip()

        if choice == "1":
            service_engineer_crud(session_token)
        elif choice == "2":
            travellers_crud_menu(session_token)
        elif choice == "3":
            scooter_management_menu(session_token)
        elif choice == "4":
            create_backup(session_token)
        elif choice == "5":
            restore_backup(session_token)
        elif choice == "6":
            read_log()
            log_activity(session_token, "Viewed Logs")
        elif choice == "7":
            print("Logging out.")
            break
        else:
            print("Invalid choice.")
