import os
import shutil
import zipfile
from datetime import datetime

DB_PATH = 'urban_mobility.db'
BACKUP_FOLDER = 'backups/'


def create_backup():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"backup_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_FOLDER, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(DB_PATH, arcname='data.db')

    print(f"Backup created: {zip_path}")
    return zip_path


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
    for backup in backups:
        print(f"- {backup}")