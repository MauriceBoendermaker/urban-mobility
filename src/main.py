from src.auth.login import Login
from src.utils.sessions import is_session_valid
from src.menus import super_admin_menu, system_admin_menu, service_engineer_menu


def main():
    while True:
        result = Login()
        if result is None:
            continue

        user, session_token = result

        while is_session_valid(session_token):
            if user[3] == "super_admin":
                super_admin_menu.super_admin_menu(session_token)
                break

            elif user[3] == "system_admin":
                system_admin_menu.system_admin_menu(session_token)
                break

            elif user[3] == "service_engineer":
                service_engineer_menu.service_engineer_menu(session_token)
                break
        else:
            print("Your session is expired")

        print("\nReturning to login screen...\n")


if __name__ == "__main__":
    main()
