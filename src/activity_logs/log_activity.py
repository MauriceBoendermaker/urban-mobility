from datetime import datetime
from .LogEntry import LogEntry
from .write_log import write_log
from src.managers.get_user import get_user
from src.utils.sessions import get_user_id_from_session


def log_activity(session_token, Description, additional_info=None, suspicious=False):
    # No, Date,  Time,  Username, Description of activity, Additional Information, Suspicious

    Date = datetime.now().strftime('%d-%m-%Y')
    Time = datetime.now().strftime('%H:%M:%S')
    user_id = get_user_id_from_session(session_token)
    user_role = None
    user_name = None
    if user_id == 0:  # If admin
        user_role = 'super_admin'
        user_name = 'super_admin'
    else:
        user = get_user(user_id)
        user_role = user['role'] if user else None
        user_name = user['username'] if user else None

    log_entry = LogEntry(
        number=0,  # auto_incremented later
        date=Date,
        time=Time,
        username=user_name,
        user_role=user_role,
        description=Description,
        additional_info=additional_info,
        suspicious=suspicious
    )
    write_log(log_entry)


def log_Logins(username, password, description, suspicious):
    Date = datetime.now().strftime('%d-%m-%Y')
    Time = datetime.now().strftime('%H:%M:%S')
    log_entry = LogEntry(
        number=0,
        date=Date,
        time=Time,
        username=username,
        description=description,
        additional_info=f"A (valid) password was used to log in.",
        suspicious=suspicious
    )
    write_log(log_entry)