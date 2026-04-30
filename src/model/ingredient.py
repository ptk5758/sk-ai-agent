from pydantic import BaseModel

class Ingredient():
    def __init__(self, id: int, name: str, quantity: int, unit: str, category:str, location: str, expiration_date: str, created_at: str, updated_at: str):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.category = category
        self.location = location
        self.expiration_date = expiration_date
        self.created_at = created_at
        self.updated_at = updated_at