from fastapi import Request, HTTPException, status
from app.http.session.session_utils import is_valid_session, session, SessionData
from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


white_list_get = ["/docs", "/openapi.json"]
white_list_post = ["/login", "/signup"]


def validate(method: str, path: str, request: Request):
    if method == "POST":
        if path not in white_list_post:
            session_id = request.cookies.get("session-id")
            print(session_id)
            if not session_id or not is_valid_session(session_id):
                print("invalid session")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


    elif method == "GET":
        if path not in white_list_get:
            session_id = request.cookies.get("session-id")
            if not session_id or not is_valid_session(session_id):
                print("invalid session")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if path.split("/")[1] == "admin":
        session_id = request.cookies.get("session-id")
        session_data: SessionData = session.get(session_id)
        print(session_data.id)
        print(session_data.authority)
        if session_data.authority != "ROLE_ADMIN":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def get_path(request: Request) -> str:
    url = str(request.url)
    base_url = str(request.base_url)
    path = url.replace(base_url, "/")
    return path
