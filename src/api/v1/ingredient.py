from fastapi import APIRouter
from src.ingredient.service import get_ingredients, create_ingredient
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from src.ingredient.dto import ChatRequest, CreateIngredientRequest
from src.ingredient.tool import select_ingredients
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

router = APIRouter(prefix="/ingredient")

# @router.post("/chat")
# def get_ingredient(chat_request: ChatRequest):
#     model = init_chat_model("google_genai:gemini-2.5-flash-lite")
#     model_with_tools = model.bind_tools([select_ingredients])

#     # 1. 사용자 메시지
#     human_message = HumanMessage(content=chat_request.message)

#     # 2. 모델 호출 (ToolCall 생성)
#     ai_message = model_with_tools.invoke([human_message])

#     tool_messages = []

#     # 3. Tool 실행
#     for tool_call in ai_message.tool_calls:
#         if tool_call["name"] == "select_ingredients":
#             result = select_ingredients.invoke(tool_call["args"])

#             tool_messages.append(
#                 ToolMessage(
#                     content=str(result),
#                     tool_call_id=tool_call["id"],
#                 )
#             )

#     # 4. Tool 결과 반영
#     if tool_messages:
#         response = model_with_tools.invoke([
#             human_message,
#             ai_message,
#             *tool_messages # array 를 풀어서 넣음 [[1,2], [3,4]] => [1,2,3,4]
#         ])
#         return response

#     return ai_message

@router.post("/agent")
def get_ingredient(chat_request: ChatRequest):
    agent = create_agent("openai:gpt-5.4-mini", tools=[select_ingredients])
    result = agent.invoke({"messages": [
        SystemMessage("당신은 냉장고 재고 관리 Agent 이다"),
        HumanMessage(chat_request.message)
        ]})
    print(result)
    return result


@router.post("/create_ingredient")
def post_ingredient(create_request: CreateIngredientRequest):
    result = create_ingredient(
        name=create_request.name,
        quantity=create_request.quantity,
        unit=create_request.unit
        )
    
    print(result)
    return result