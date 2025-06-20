from .LogEntry import LogEntry
import csv
import os
from utils.encryption import deterministic_decrypt, deterministic_encrypt
from .Read_log import decrypt_row
Logs_file = "logs/Logs.csv"


def write_log(log_entry: LogEntry):
    log_entry.number = get_last_log_entry_number() + 1
    # Ensure the logs directory exists

    if not os.path.exists('logs'):
        os.makedirs('logs')

    headers = ['No', 'Date', 'Time', 'Username', 'User Role',
               'Description', 'Additional Info', 'Suspicious']

    # Check if the file exists, if not create it with headers
    if not os.path.isfile(Logs_file) or os.path.getsize(Logs_file) == 0:
        with open(Logs_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([deterministic_encrypt(header)
                            for header in headers])

    with open(Logs_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        properties = [log_entry.number, log_entry.date, log_entry.time, log_entry.username,
                      log_entry.user_role, log_entry.description, log_entry.additional_info, log_entry.suspicious]
        writer.writerow(deterministic_encrypt(prop) for prop in properties)


def get_last_log_entry_number() -> int:
    try:
        with open(Logs_file, mode='r') as file:
            reader = csv.DictReader(file)
            last_row = None
            for row in reader:
                last_row = row

        if last_row:
            last_row = decrypt_row(last_row)
            return int(last_row['No'])
        return 0
    except FileNotFoundError:
        return 0
    except Exception:
        print("Error reading log file.")
        return 0
