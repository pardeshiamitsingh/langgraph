from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import json


from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

tavily_search_tool = TavilySearchResults(search_depth="basic")

llm_with_tools = llm.bind_tools([tavily_search_tool])

class ChatbotState(TypedDict):
    """A simple chatbot that responds to user input."""
    messages: Annotated[list, add_messages]

def chatbot(state: ChatbotState):
    """A simple chatbot that responds to user input."""
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response]
    }

def tool_handler(state: ChatbotState):
    print("Tool handler invoked with state:", state["messages"][-1].content)
    """Handles tool calls and returns the response."""
    last_message = state["messages"][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return END

graph = StateGraph(ChatbotState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
tools = [tavily_search_tool]
tool_node = ToolNode(tools=tools)
graph.add_node("tool_node", tool_node)
graph.add_conditional_edges("chatbot", tool_handler)
graph.add_edge("tool_node", "chatbot")
app = graph.compile()
print("Chatbot with tools is ready! Type 'exit' or 'quit' to stop the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break
    response = app.invoke({"messages": [HumanMessage(content=user_input)]})
    ##write response to a json file
    with open("chatbot_response.json", "w") as f:
        json.dump(response, f)

    print(f"Bot: {response['messages']}")
