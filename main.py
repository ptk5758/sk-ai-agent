from fastapi import FastAPI
from dotenv import load_dotenv
from src.api.v1.common import router as common_router
from src.api.v1.ingredient import router as ingredient_router
load_dotenv()

app = FastAPI()

app.include_router(common_router)
app.include_router(ingredient_router)