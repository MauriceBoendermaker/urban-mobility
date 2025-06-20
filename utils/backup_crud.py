import sqlite3
from .Sessions import get_user_id_from_session
from datetime import datetime
from .encryption import generate_backup_code
DB_PATH = "urban_mobility.db"


def add_backup_to_db(backup_file, session_token, SystemAdminID):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    current_user_id = get_user_id_from_session(session_token)
    if current_user_id is None:
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
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (backup_file, "super_admin", datetime.now().strftime('%Y%m%d'), backup_code, False, SystemAdminID, False))

    conn.commit()
    conn.close()
    print(f"Backup {backup_file} added to database. Backup code: {backup_code}")


def add_backup_as_system_admin(backup_file, session_token, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    current_user_id = get_user_id_from_session(session_token)
    if current_user_id is None:
        print("No valid session found. Cannot add backup.")
        return

    # Insert the backup file entry
    cursor.execute('''INSERT INTO backups (filename, created_by, datetime, one_use_code, used, allowed_user, revoked)
                      VALUES (?, ?, ?, ?, ?, ?)''', (backup_file, username, datetime.now().strftime('%Y%m%d'), None, False, None, False))

    conn.commit()
    conn.close()


def generate_backup_code_for_system_admin(session_token, backup_file, SystemAdminID):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    backup_code = generate_backup_code()
    if session_token is None:
        print("No valid session found. Cannot assign backup.")
        return

    cursor.execute('''UPDATE backups
                      SET one_use_code = ?
                      WHERE filename = ? AND allowed_user = ?''',
                   (backup_code, backup_file, SystemAdminID))
    print(
        f"Backup code {backup_code} generated for system admin {SystemAdminID} for backup file {backup_file}.")

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
