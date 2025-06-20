from utils.Sessions import get_user_id_from_session
from managers.system_admin_manager import get_user
from datetime import datetime
from .write_log import write_log
from .LogEntry import LogEntry


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


def log_Logins():
    # This function should log user login activities
    pass  # Implement the logic to log login activities here