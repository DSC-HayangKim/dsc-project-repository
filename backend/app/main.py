from fastapi import FastAPI
from app.models import *
from app.api.v1.api import api_router
from app.core.embedding import get_model

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def load_models_on_startup():
    get_model()
    print('Model loaded on startup')
