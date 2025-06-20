import time
import secrets

SESSION_DURATION = 60
SESSIONS = {}


def create_session(user_id: int):
    session_token = secrets.token_hex(16)
    expiration = time.time() + SESSION_DURATION
    SESSIONS[session_token] = {'user_id': user_id, 'expires': expiration}
    print(f"[DEBUG] Created session {session_token} for user_id {user_id}")
    return session_token


def is_session_valid(token):
    session = SESSIONS.get(token)
    if session and session['expires'] > time.time():
        session['expires'] = time.time() + SESSION_DURATION
        return True
    return False


def get_user_id_from_session(token):
    print(f"[DEBUG] SESSIONS: {SESSIONS}")
    session = SESSIONS.get(token)
    if session:
        return session['user_id']
    return None
