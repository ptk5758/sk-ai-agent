from src.model.ingredient import Ingredient
from src.repositorie.ingredient import get_ingredients as get
def get_ingredients() -> list[Ingredient] :
    result = get()
    return result