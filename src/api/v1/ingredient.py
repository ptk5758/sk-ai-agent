from fastapi import APIRouter
from src.dto.ingredient import GetIngredients
from src.service.ingredient import get_ingredients
router = APIRouter(prefix="/ingredient")

@router.get("")
def get_ingredient():
    list = get_ingredients()
    return list