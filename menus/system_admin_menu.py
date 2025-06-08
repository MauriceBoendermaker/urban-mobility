from managers.service_engineer_manager import service_engineer_crud


def system_admin_menu():
    while True:

        print("\n--- System Admin Menu ---")
        print("1. Manage Service Engineers")
        print("2. Logout")
        choice = input("Choose option: ").strip()
        if choice == "1":
            service_engineer_crud()
        elif choice == "2":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
