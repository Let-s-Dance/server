from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from . import models
from .database import engine
from .routers.admin import admin_router
from .routers.login import login_router
from .routers.musicvideo import music_video_router
from .routers.signup import signup_router
from .routers.thumbnail import thumbnail_router
from .routers.user import user_router
from .routers.game import game_router
from app.middleware import get_path, validate
from fastapi_utilities import repeat_every
from app.http.session import session, SessionData
from datetime import datetime

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(admin_router.router)
app.include_router(login_router.router)
app.include_router(music_video_router.router)
app.include_router(signup_router.router)
app.include_router(user_router.router)
app.include_router(thumbnail_router.router)
app.include_router(game_router.router)



@app.middleware("http")
async def check_session(request: Request, call_next):
    method = request.method
    path = get_path(request)
    try:
        validate(method, path, request)
        response = await call_next(request)
        return response
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "로그인이 필요합니다."})
        if e.status_code == status.HTTP_403_FORBIDDEN:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "권한이 없습니다.."})


@app.on_event("startup")
@repeat_every(seconds=60 * 30)
def remove_expired_sessions():
    keys = session.keys()
    for key in keys:
        session_data: SessionData = session.get(key)
        updated_at = session_data.time
        diff = datetime.now() - updated_at
        if diff.total_seconds() > 60 * 30:
            del session[key]
