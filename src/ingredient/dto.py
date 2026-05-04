from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class CreateIngredientRequest(BaseModel):
    name: str
    quantity: float
    unit: str