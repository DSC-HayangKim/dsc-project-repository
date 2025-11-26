from fastapi import APIRouter
from app.api.v1.endpoints import auth, user, agent, threads, chat, test
from app.api.deps import get_current_user_payload
from fastapi import Depends

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(user.router, prefix="/user", tags=["user"])

api_router.include_router(agent.router, prefix="/agent", tags=["agent"],
        dependencies=[Depends(get_current_user_payload)])

api_router.include_router(threads.router, prefix="/threads", tags=["threads"],
        dependencies=[Depends(get_current_user_payload)])

api_router.include_router(chat.router, prefix="/chat", tags=["chat"],
        dependencies=[Depends(get_current_user_payload)])

api_router.include_router(test.router, prefix="/test", tags=["test"])
