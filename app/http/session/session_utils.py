from app.http.session import session, SessionData
from datetime import datetime


def is_valid_session(session_id: str) -> bool:
    if session_id not in session.keys():
        return False
    session_data: SessionData = session.get(session_id)
    updated_at = session_data.created_at
    now = datetime.now()

    diff = now - updated_at
    print(updated_at, now, diff)
    if diff.total_seconds() > 1800:
        return False

    return True


def update_session(session_id: str) -> None:
    session_data: SessionData = session.get(session_id)
    session_data.created_at = datetime.now()
    session[session_id] = session_data


def get_id_from_session(session_id: str) -> int:
    session_data: SessionData = session.get(session_id)
    return session_data.id
