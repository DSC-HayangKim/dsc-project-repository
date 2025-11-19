from fastapi import APIRouter
from app.api.v1.endpoints import threads

api_router = APIRouter()
api_router.include_router(threads.router, prefix="/threads", tags=["threads"])
