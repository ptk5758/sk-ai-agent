from fastapi import APIRouter
from src.ingredient.service import get_ingredients

router = APIRouter(prefix="/ingredient")

@router.get("")
def get_ingredient():
    list = get_ingredients()
    return list