import os
import csv

from .LogEntry import LogEntry
from utils.encryption import deterministic_decrypt

Logs_file = "logs/Logs.csv"


def read_log():
    if not os.path.exists(Logs_file):
        print("Log file does not exist.")
        return
    Headers = []
    Entries = []
    with open(Logs_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        Headers = reader.fieldnames
        for row in reader:
            decrypted_row = decrypt_row(row)
            entry = LogEntry(
                number=int(decrypted_row['No']),
                date=decrypted_row['Date'],
                time=decrypted_row['Time'],
                username=decrypted_row['Username'],
                user_role=decrypted_row['User Role'],
                description=decrypted_row['Description'],
                additional_info=decrypted_row['Additional Info'],
                suspicious=decrypted_row['Suspicious'] == 'True'
            )
            Entries.append(entry)
    if not Headers or not Entries:
        print("No logs found.")
        return

    Headers = decrypt_headers(Headers)

    print(formatted_logs(Headers, Entries))


def formatted_logs(headers, entries):
    rows = [headers] + [list(map(str, entry.__dict__.values()))
                        for entry in entries]

    cols = list(zip(*rows))  # Transpose the rows to columns
    col_widths = [max(len(item) for item in col) for col in cols]

    formatted = []
    for row in rows:
        formatted_row = " | ".join(item.ljust(width)
                                   for item, width in zip(row, col_widths))
        formatted.append(formatted_row)

    return "\n".join(formatted)


def decrypt_headers(headers):
    headers = [deterministic_decrypt(header) for header in headers]
    return headers


def decrypt_row(entries):
    row = {deterministic_decrypt(key): deterministic_decrypt(
        value) for key, value in entries.items()}

    entries.clear()
    entries.update(row)
    return entries
