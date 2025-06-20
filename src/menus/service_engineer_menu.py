from src.auth.auth_manager import update_own_password, delete_own_account
from src.managers.scooter_manager import scooter_management_menu
from src.utils.sessions import get_user_id_from_session


def service_engineer_menu(session_token):
    while True:
        print("\n--- Service Engineer Menu ---")
        print("1. Manage Scooters")
        print("2. Change Own Password")
        print("3. Delete your account")

        print("4. Logout")
        choice = input("Choose option: ").strip()

        user_id = get_user_id_from_session(session_token)

        if choice == "1":
            scooter_management_menu(session_token)
        elif choice == "2":
            update_own_password(user_id)
        elif choice == "3":
            if delete_own_account(user_id):
                print("Logging out.")
                break

        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
