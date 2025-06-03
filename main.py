# from auth.login import login

from managers.system_admin_manager import system_admin_crud


def main():
    user = None
    # while not user:
    #     user = login()

    while True:
        # if user["role"] == "super_admin":
        print("\n--- Super Admin Menu ---")
        print("1. Manage System Administrators")
        print("2. View Logs (komt binnenkort)")
        print("3. Logout")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            system_admin_crud()
        elif choice == "2":
            print("Logs komt hierna.")
        elif choice == "3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
