from langchain.tools import tool
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

from src.ingredient.service import get_ingredients, create_ingredient

class Ingredient(BaseModel):
    id: UUID
    name: str
    quantity: float
    unit: str
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
                created_at=row[4],
                updated_at=row[5],
            )
        )
    return result

@tool
def append_ingredient(name: str, quantity: float, unit: str) -> UUID:
    """
    새로운 식재료를 DB에 추가하는 함수.

    Args:
        name (str): 식재료 이름
        quantity (float): 수량
        unit (str): 단위 (예: g, ml, 개 등)

    Returns:
        UUID: 생성된 식재료의 고유 ID
    """
    uuid = create_ingredient(name=name, quantity=quantity, unit=unit)
    return uuid