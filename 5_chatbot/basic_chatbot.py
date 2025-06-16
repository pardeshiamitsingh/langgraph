from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
class BasichatState(TypedDict):
    """A simple chatbot that responds to user input."""

    messages: Annotated[list, add_messages]


def basic_chatbot(state: BasichatState):
    return  {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasichatState)

graph.add_node("chatbot", basic_chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()
print("Chatbot is ready! Type 'exit' or 'quit' to stop the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break
    response = app.invoke({"messages": [HumanMessage(content=user_input)]})
    print(f"Bot: {response['messages']}")

    