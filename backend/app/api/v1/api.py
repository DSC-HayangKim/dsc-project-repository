from fastapi import APIRouter
from app.api.v1.endpoints import threads, auth, user

api_router = APIRouter()
api_router.include_router(threads.router, prefix="/threads", tags=["threads"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
