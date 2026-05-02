from fastapi import APIRouter
from src.ingredient.service import get_ingredients
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage
from src.ingredient.dto import ChatRequest
from src.ingredient.tool import select_ingredients

router = APIRouter(prefix="/ingredient")

@router.post("/chat")
def get_ingredient(chat_request: ChatRequest):
    model = init_chat_model("google_genai:gemini-2.5-flash-lite")
    model_with_tools = model.bind_tools([select_ingredients])

    # 1. 사용자 메시지
    human_message = HumanMessage(content=chat_request.message)

    # 2. 모델 호출 (ToolCall 생성)
    ai_message = model_with_tools.invoke([human_message])

    tool_messages = []

    # 3. Tool 실행
    for tool_call in ai_message.tool_calls:
        if tool_call["name"] == "select_ingredients":
            result = select_ingredients.invoke(tool_call["args"])

            tool_messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    # 4. Tool 결과 반영
    if tool_messages:
        response = model_with_tools.invoke([
            human_message,
            ai_message,
            *tool_messages # array 를 풀어서 넣음 [[1,2], [3,4]] => [1,2,3,4]
        ])
        return response

    return ai_message