import sqlite3

from datetime import datetime
from .sessions import is_session_valid
from .encryption import generate_backup_code

DB_PATH = "urban_mobility.db"


def add_backup_to_db(backup_file, session_token, SystemAdminID):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not is_session_valid(session_token):
        print("No valid session found. Cannot add backup.")
        return

    backup_code = generate_backup_code()
    # Insert the backup file entry
    ''''filename TEXT,
        created_by TEXT,
        datetime TEXT,
        one_use_code TEXT,
        used INTEGER DEFAULT 0,
        allowed_user TEXT
    );
'''

    cursor.execute('''INSERT INTO backups (filename, created_by, datetime, one_use_code, used, allowed_user, revoked)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (
    backup_file, "super_admin", datetime.now().strftime('%Y%m%d'), backup_code, False, SystemAdminID, False))

    conn.commit()
    conn.close()
    print(f"Backup {backup_file} added to database. Backup code: {backup_code}")


def add_backup_as_system_admin(backup_file, session_token, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not is_session_valid(session_token):
        print("No valid session found. Cannot add backup.")
        return

    # Insert the backup file entry
    cursor.execute('''INSERT INTO backups (filename, created_by, datetime, one_use_code, used, allowed_user, revoked)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (backup_file, username, datetime.now().strftime('%Y%m%d'), None, False, None, False))

    conn.commit()
    conn.close()


def generate_backup_code_for_system_admin(session_token, backup_file, SystemAdminID):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    backup_code = generate_backup_code()
    if session_token is None:
        print("No valid session found. Cannot assign backup.")
        return

    print(f"backup_file: {backup_file}, SystemAdminID: {SystemAdminID}")
    cursor.execute('''UPDATE backups
                      SET one_use_code = ?, allowed_user = ?
                      WHERE filename = ?''',
                   (backup_code, SystemAdminID, backup_file))
    print(
        f"UPDATE backups SET one_use_code = {backup_code}, allowed_user = {SystemAdminID} WHERE filename = {backup_file}")

    conn.commit()
    conn.close()


def RevokeBackup(backup_file):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''UPDATE backups
                      SET revoked = 1
                      WHERE filename = ?''', (backup_file,))

    conn.commit()
    conn.close()


def is_restore_allowed(filename, code, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM backups
                      WHERE filename = ? ''', (filename,))
    backup = cursor.fetchone()
    filename, one_use_code, used, allowed_user, revoked = backup[
        1], backup[4], backup[5], backup[6], backup[7]
    if backup is None:
        print("Invalid backup file or code.")
        return False

    conn.close()
    return used == 0 and int(allowed_user) == user_id and one_use_code == code and not revoked
