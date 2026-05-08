from fastapi import FastAPI
from dotenv import load_dotenv
from src.api.v1.ingredient import router as ingredient_router
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 허용할 도메인 목록
    allow_credentials=True,           # 쿠키 포함 여부 설정
    allow_methods=["*"],              # 모든 HTTP Method 허용 (GET, POST 등)
    allow_headers=["*"],              # 모든 HTTP Header 허용
)

app.include_router(ingredient_router)