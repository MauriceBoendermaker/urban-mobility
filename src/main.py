from src.auth.login import Login
from src.utils.sessions import is_session_valid
from src.menus import super_admin_menu, system_admin_menu, service_engineer_menu
from src.activity_logs.read_log import print_suspicious_logs
from src.activity_logs.log_activity import log_Logins


def main():
    while True:
        result = Login()
        if result is None:
            continue

        user, session_token, suspicious_activities = result
        if suspicious_activities:
            log_Logins(*suspicious_activities)

        while is_session_valid(session_token):
            if user[3] == "super_admin":

                print_suspicious_logs()
                super_admin_menu.super_admin_menu(session_token)
                break

            elif user[3] == "system_admin":
                print_suspicious_logs()
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
