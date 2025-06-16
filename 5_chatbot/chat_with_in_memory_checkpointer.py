from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

llm = ChatGroq(model="llama-3.1-8b-instant")

class ChatbotState(TypedDict):
    """A simple chatbot that responds to user input."""
    messages: Annotated[list, add_messages]

def chatbot(state: ChatbotState):
    """A simple chatbot that responds to user input."""
    response = llm.invoke(state["messages"])
    return {
        "messages": [response]
    }

config = {"configurable": {
                "thread_id": "1"
            }   
        }

graph = StateGraph(ChatbotState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)
# Add memory checkpointing
app = graph.compile(checkpointer=memory)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break
    response = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

    
    # Save the response to memory
    #memory.save_state(response)
    
    print(f"Bot: {response['messages'][-1].content}")  # Print the last message content

