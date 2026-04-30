from pydantic import BaseModel
from src.model.ingredient import Ingredient

class GetIngredients(BaseModel):
    list: list[dict]