from fastapi import FastAPI, Request, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from app.routers import user, login, music
from . import models, schemas
from .database import engine
from fastapi_utilities import repeat_every
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user.router)
app.include_router(login.router)
app.include_router(music.router)


@app.middleware("http")
async def check_session(request: Request, call_next):
    print("check_validation :", request.url)
    method = request.method
    path = get_path(request)

    try:
        validate(method, path, request)
        response = await call_next(request)
        return response
    except HTTPException:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "로그인이 필요합니다."})


def validate(method: str, path: str, request: Request):
    if method == "POST":
        if path not in login.white_list_post:
            session_id = request.cookies.get("session-id")
            if not session_id or not login.is_valid_session(session_id):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    elif method == "GET":
        if path not in login.white_list_get:
            session_id = request.cookies.get("session-id")
            if not session_id or not login.is_valid_session(session_id):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
def get_path(request: Request) -> str:
    url = str(request.url)
    base_url = str(request.base_url)
    path = url.replace(base_url, "/")
    return path

@app.on_event("startup")
@repeat_every(seconds=60 * 30)
def remove_expired_sessions():
    session = login.session
    keys = session.keys()
    for key in keys:
        session_data : schemas.SessionData = session.get(key)
        updated_at = session_data.time
        diff = datetime.now() - updated_at
        if diff.total_seconds() > 60 * 30:
            del session[key]


@app.get("/")
def main_page(request: Request):
    session_id : str = request.cookies.get("session-id")
    session_data : schemas.SessionData= login.session.get(session_id)
    user_id = session_data.user_id
    print(user_id)
    return "main page"


