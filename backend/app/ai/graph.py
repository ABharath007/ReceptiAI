from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_groq import ChatGroq
from dotenv import load_dotenv

from langchain_core.messages import SystemMessage

from app.ai.state import ReceptionState
from app.ai.prompts import SYSTEM_PROMPT

from app.ai.tools import (
    search_business_knowledge,
    find_available_slots,
    book_appointment,
    find_resources_by_service,
    find_services_by_resource,
    find_resource_by_name,
    find_customer_by_phone,
    find_service_by_name,
    create_customer,
    raise_ticket,
    close_ticket,
    list_open_tickets
    
)

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

tools = [
    search_business_knowledge,
    find_available_slots,
    book_appointment,
    find_resources_by_service,
    find_services_by_resource,
    find_resource_by_name,
    find_service_by_name,
    find_customer_by_phone,
    create_customer,
    raise_ticket,
    close_ticket,
    list_open_tickets
]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: ReceptionState):
    print("Entered chatbot")
    print(state)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    print("Calling LLM")

    response = llm_with_tools.invoke(messages)

    print("Response:")
    print(response)

    print("Tool calls:")
    print(response.tool_calls)

    return {
        "messages": [response]
    }
    
tool_node = ToolNode(tools)
graph = StateGraph(ReceptionState)

graph.add_node(
    "chatbot",
    chatbot
)

graph.add_node(
    "tools",
    tool_node
)

graph.set_entry_point("chatbot")

graph.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
graph.add_edge(
    "tools",
    "chatbot"
)
reception_graph = graph.compile()