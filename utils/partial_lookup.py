import sqlite3
from encryption import decrypt
from typing import List

DB_PATH = "urban_mobility.db"


def partial_lookup(table: str, column: str, partial: str, decrypt_results: bool = False) -> List[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {column} LIKE ?", ('%' + partial + '%',))
    results = cursor.fetchall()
    conn.close()

    if decrypt_results:
        decrypted_results = []
        for row in results:
            decrypted_row = tuple(decrypt(cell) if isinstance(cell, str) else cell for cell in row)
            decrypted_results.append(decrypted_row)
        return decrypted_results

    return results
