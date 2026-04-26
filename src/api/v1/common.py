from fastapi import APIRouter
from src.service.common import get_information, chat
from src.dto.sample import SampleResponse
from src.dto.common import ChatRequest, ChatResponse

router = APIRouter(prefix="/common")

@router.get("", response_model=SampleResponse)
def get_common() -> SampleResponse:
    info = get_information()
    return SampleResponse(message=info.message)

@router.post("/chat", response_model=ChatResponse)
def get_chat(chat_request: ChatRequest) -> ChatResponse:
    agent_response = chat(chat_request.message)
    return ChatResponse(message=agent_response.content)