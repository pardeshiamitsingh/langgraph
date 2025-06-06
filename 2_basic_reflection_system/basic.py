from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from chains import generate_chain, reflect_chain
from langgraph.graph import MessageGraph, END, START

load_dotenv()

graph = MessageGraph()

RELECT = "reflect"
GENERATE = "generate"

def generate_node(state) -> List[BaseMessage]:
    """Generate a joke based on the topic."""
    return generate_chain.invoke({
            "messages": state
            }
    )

def reflect_node(state):
    """Reflect on the joke and provide feedback."""
    response = reflect_chain.invoke({
        "messages": state
    })
    return [HumanMessage(content=response.content)]


graph.add_node(
    GENERATE,
    generate_node
)
   
graph.add_node(
    RELECT,
    reflect_node
)


graph.set_entry_point(
    GENERATE
)

def should_continue(state):
    print("Current state:", len(state))
    if len(state) > 4:
        print("Reached maximum iterations, ending the process.")
        return END
    
    return RELECT


graph.add_conditional_edges(
    GENERATE,
    should_continue
)


graph.add_edge(RELECT, GENERATE)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

response = app.invoke( HumanMessage(content="Tell me a joke about the topic math."))

print(response)