from .backup_crud import add_backup_to_db, add_backup_as_system_admin, generate_backup_code_for_system_admin, RevokeBackup
import os
import shutil
import zipfile
from datetime import datetime
from menus.Choose_system_admin import choose_system_admin
from managers.system_admin_manager import get_user
from .Sessions import get_user_id_from_session, is_session_valid
DB_PATH = 'urban_mobility.db'
BACKUP_FOLDER = '../backups/'


def create_backup(session_token):

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"backup_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_FOLDER, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(DB_PATH, arcname='data.db')

    # call add_backup_to_db to add the backup entry to the database
    print(f"Backup created: {zip_path}")
    print("Adding backup to database...")

    current_user_id = get_user_id_from_session(session_token)
    if current_user_id is None:
        print("No valid session found. Cannot add backup.")
        return
    if current_user_id == 0:

        SystemAdminID = choose_system_admin()
        if SystemAdminID is None:
            print("No system admin selected. Backup will not be added to the database.")
        else:
            add_backup_to_db(zip_filename, session_token, SystemAdminID)
    else:
        user = get_user(current_user_id)
        if user is None:
            print("No valid user found. Cannot add backup.")
            return
        else:
            if user['role'] == 'system_admin':
                add_backup_as_system_admin(
                    zip_filename, session_token, user['username'])
                print(
                    f"Backup {zip_filename} added to database by {user['username']}.")
            else:
                print(f"Cannot add backup to database as a {user['role']}")

    return zip_path


def assign_backup_to_system_admin(session_token):
    if is_session_valid(session_token):
        backup_file = choose_backup_file()

        SystemAdminID = choose_system_admin()
        if SystemAdminID is None:
            print("No system admin selected. Backup will not be assigned.")
            return

        generate_backup_code_for_system_admin(
            backup_file, session_token, SystemAdminID)


def restore_backup(backup_file):
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} does not exist.")
        return

    with zipfile.ZipFile(backup_file, 'r') as zipf:
        zipf.extractall(BACKUP_FOLDER)

    print(f"Backup restored from {backup_file}.")
    # Optionally, you can also copy the restored DB to the original location
    shutil.copy(os.path.join(BACKUP_FOLDER, 'data.db'), DB_PATH)
    print("Database restored to original location.")


def list_backups():
    if not os.path.exists(BACKUP_FOLDER):
        print("No backups found.")
        return

    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith('.zip')]
    if not backups:
        print("No backups found.")
        return

    print("Available backups:")
    for index, backup in enumerate(backups):
        print(f"{index + 1}- {backup}")

    return backups


def choose_backup_file():
    backups = list_backups()
    if not backups:
        return None

    while True:
        choice = input(
            "Choose a backup to restore (number or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            return None
        try:
            index = int(choice) - 1
            if 0 <= index < len(backups):
                print(f"You selected: {backups[index]}")
                return backups[index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")


def Revoke_Backup():
    backup_file = choose_backup_file()
    RevokeBackup(backup_file)
    print(f"Backup {backup_file} has been revoked from the system admin.")
