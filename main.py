from fastapi import FastAPI
from src.api.v1.common import router as common_router

app = FastAPI()

app.include_router(common_router)