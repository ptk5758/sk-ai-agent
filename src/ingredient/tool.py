from langchain.tools import tool
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

from src.ingredient.service import get_ingredients

class Ingredient(BaseModel):
    id: UUID
    name: str
    quantity: float
    unit: str
    category: str
    location: str
    expiration_date: date
    created_at: datetime
    updated_at: datetime

@tool
def select_ingredients() -> list[Ingredient]:
    """
    DB에서 냉장고의 재고를 반환 하는 함수
    """
    list = get_ingredients()
    result = []
    for row in list:
        result.append(
            Ingredient(
                id=row[0],  # UUID 그대로 가능
                name=row[1],
                quantity=row[2],
                unit=row[3],
                category=row[4],
                location=row[5],
                expiration_date=row[6],
                created_at=row[7],
                updated_at=row[8],
            )
        )
    return result