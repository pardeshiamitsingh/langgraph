from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    """
    A simple state representation using TypedDict.
    """
    count: int

def increment(state: State) -> State:
    """
    Increment the count in the state by 1.
    
    Args:
        state (State): The current state.
    
    Returns:
        State: The updated state with incremented count.
    """
    return {
        'count': state['count'] + 1
    }

def should_continue(state: State):
    """
    Check if the count in the state is less than 10.
    
    Args:
        state (State): The current state.
    
    Returns:
        bool: True if count is less than 10, False otherwise.
    """
    if state['count'] < 10:
        print(f"Current count: {state['count']}")
        return "continue"
    else:
        print(f"Final count reached: {state['count']}")
        return "end"
    
# Define the state graph
graph = StateGraph(State)

graph.add_node("increment", increment)
graph.add_conditional_edges("increment", should_continue, {
    "continue": "increment",
    "end": END
})

graph.set_entry_point("increment")

app = graph.compile()


# Run the state graph
if __name__ == "__main__":
    print("Starting state graph...")
    init_state = {
        'count': 0
    }
    response = app.invoke(init_state)
    print("Final state:", response)
    print("State graph execution completed.")