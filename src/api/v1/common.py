from fastapi import APIRouter
from src.service.common import get_information
from src.dto.sample import SampleResponse

router = APIRouter(prefix="/common")

@router.get("", response_model=SampleResponse)
def get_common() -> SampleResponse:
    info = get_information()
    return SampleResponse(message=info.message)