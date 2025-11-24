from fastapi import FastAPI
from app.models import *
from app.api.v1.api import api_router
from app.core.embedding import get_model

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def load_models_on_startup():
    get_model()
    print('Model loaded on startup')
