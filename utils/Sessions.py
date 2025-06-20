import secrets
import time

SESSION_DURATION = 60
SESSIONS = {}


def create_session(user_id: int):
    session_token = secrets.token_hex(16)
    expiration = time.time() + SESSION_DURATION
    SESSIONS[session_token] = {'user_id': user_id, 'expires': expiration}
    return session_token


def is_session_valid(token):
    session = SESSIONS.get(token)
    if session and session['expires'] > time.time():
        return True
    return False


def get_user_id_from_session(token):
    session = SESSIONS.get(token)
    if session and session['expires'] > time.time():
        return session['user_id']
    return None
