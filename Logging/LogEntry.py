from dataclasses import dataclass
from utils.encryption import deterministic_decrypt


@dataclass
class LogEntry:
    def __init__(self, number, date, time,  description, username=None, user_role=None, additional_info=None, suspicious=False):
        self.number = number
        self.date = date
        self.time = time
        self.username = username
        self.user_role = user_role
        self.description = description
        self.additional_info = additional_info
        self.suspicious = suspicious
