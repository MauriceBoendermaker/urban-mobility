from auth.login import Login
from utils.Sessions import is_session_valid
from managers.service_engineer_manager import service_engineer_crud
from menus import super_admin_menu, system_admin_menu


def main():
    result = None
    while result is None:
        result = Login()
    user, session_token = result

    while is_session_valid(session_token):

        if user[3] == "super_admin":
            super_admin_menu.super_admin_menu()
            break

        elif user[3] == "system_admin":
            super_admin_menu.super_admin_menu()
            break
    else:
        print("Your session is expired")


if __name__ == "__main__":
    main()
