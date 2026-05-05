import psycopg

from dotenv import load_dotenv

from typing import Literal
from typing_extensions import TypedDict

from uuid import UUID

from pydantic import BaseModel

from datetime import date, datetime

from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langgraph.graph import MessagesState, END, StateGraph, START
from langgraph.types import Command

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def get_ingredients():
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                        SELECT
                            id,
                            name,
                            quantity,
                            unit,
                            created_at,
                            updated_at
                        FROM ingredients
                        """)
            rows = cursor.fetchall()
    return rows

def create_ingredient(name: str, quantity: float, unit: str) -> UUID :
    with psycopg.connect("dbname=sk_ax user=dev password=dev1234 host=localhost") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO ingredients
                           (
                           "name",
                           quantity,
                           unit
                           )
                           VALUES
                           (
                           %s,
                           %s,
                           %s
                           )
                           RETURNING id
                           """,
                           (name, quantity, unit))
            return cursor.fetchone()
        
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

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

@tool
def select_recipe(text: str):
    """
    레시피 벡터 DB에서 유사한 레시피를 검색합니다.
    
    Args:
        text (str): 검색할 레시피 키워드 또는 문장
    
    Returns:
        list: 유사도 높은 상위 3개의 Document 객체 리스트
    """
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vectorstore.similarity_search(text, k=3)

llm = ChatOpenAI(model="gpt-5.4-mini")
members = ["ingredient", "cooker"]
options = members + ["FINISH"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
class State(MessagesState):
    next: str

class Router(TypedDict):
    next: Literal["ingredient", "cooker", "FINISH"]
    
def _super_visor_node(state: State) -> Command[Literal["ingredient", "cooker", "__end__"]]:
    print("\n")
    print(state)
    messages = [
        SystemMessage(content=system_prompt)
    ] + state["messages"]

    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    # return Command(goto=goto, update={"next": goto})
    return Command(
        update={
            "next": goto
        },
        goto=goto
    )

ingredient_agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[select_ingredients, append_ingredient],
    system_prompt="""
    - 당신은 냉장고 재고 관리 에이전트 이다.
    - 요리 추천은 반드시 'cooker' Agent 를 통해서 진행 할 것
    """
)

def _ingredient_node(state: State) -> Command[Literal["super_visor"]]:
    result = ingredient_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="ingredient")
            ]
        },
        goto="super_visor"
    )

cooker_agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[select_recipe],
    system_prompt="""
    - 당신은 요리 에이전트 이다.
    - Vector DB에 등록되어 있는 레시피만을 응답 해야한다. (이는 Tool 로 써 접근 가능하다)
    """
)

def _cooker_node(state: State) -> Command[Literal["super_visor"]]:
    result = cooker_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="cooker")
            ]
        },
        goto="super_visor"
    )

def solution(message: str):

    workflow = StateGraph(State)

    workflow.add_edge(START, "super_visor")
    workflow.add_node("super_visor", _super_visor_node)
    workflow.add_node("ingredient", _ingredient_node)
    workflow.add_node("cooker", _cooker_node)

    graph = workflow.compile()

    result = graph.invoke({"messages": [HumanMessage(content=message)]})

    return result