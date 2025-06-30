from src.activity_logs.read_log import read_log
from src.activity_logs.log_activity import log_activity
from src.managers.travellers_manager import travellers_crud_menu
from src.managers.scooter_manager import scooter_management_menu
from src.utils.backup_manager import create_backup, restore_backup
from src.managers.service_engineer_manager import service_engineer_crud
from src.managers.get_user import get_user
from src.utils.sessions import get_user_id_from_session
from src.auth.auth_manager import update_own_password, delete_own_account


def system_admin_menu(session_token):
    while True:
        print("\n--- System Admin Menu ---")
        print("1. Manage Service Engineers")
        print("2. Manage Travellers")
        print("3. Manage Scooters")
        print("4. Create Backup")
        print("5. Restore Backup")
        print("6. View Logs")
        print("7. Reset password")
        print("8. Delete your account")

        print("9. Logout")
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

            update_own_password(get_user_id_from_session(session_token))
            break
        elif choice == "8":

            if delete_own_account(get_user_id_from_session(session_token)):
                print("Logging out.")
                break
        elif choice == "9":
            print("activity_logs out.")
            break

        else:
            print("Invalid choice.")
