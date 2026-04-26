from langchain.chat_models import init_chat_model
from src.model.sample_message import SampleMessage

def get_information() -> SampleMessage:
    return SampleMessage("Sample Agent asd")

def chat(message: str):
    model = init_chat_model("google_genai:gemini-2.5-flash-lite")
    return model.invoke(message)