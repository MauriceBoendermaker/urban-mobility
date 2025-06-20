from auth.login import get_user
from utils.sessions import get_user_id_from_session
from scooters.scooters import add_scooter, delete_scooter, update_scooter_attributes, search_scooter, list_all_scooters


def scooter_management_menu(session_token):
    user_id = get_user_id_from_session(session_token)
    user = get_user(user_id)
    if user is None:
        print("No valid user found. Cannot access scooter management.")
        return
    role = user['role']
    while True:
        print("\n--- Scooter Management ---")
        print("1. Search scooter")
        print("2. Update scooter")
        if role != "service_engineer":
            print("3. Add new scooter")
            print("4. Delete scooter")
        print("5. List all scooters")
        print("6. Back")

        choice = input("Choose option: ").strip()

        if choice == "1":
            search_scooter(session_token)
        elif choice == "2":
            update_scooter_attributes(role, session_token)
        elif choice == "3" and role != "service_engineer":
            add_scooter(session_token)
        elif choice == "4" and role != "service_engineer":
            delete_scooter(session_token)
        elif choice == "5":
            list_all_scooters(session_token)
        elif choice == "6":
            break
        else:
            print("Invalid choice or insufficient permissions.")
