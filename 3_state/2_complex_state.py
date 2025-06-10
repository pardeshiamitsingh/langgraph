from typing import TypedDict, List, Annotated
from langgraph.graph import START, END, StateGraph
import operator

class ComplexState(TypedDict):
    """
    A complex state representation using TypedDict.
    """
    count: int
    sum: Annotated[int, operator.add]
    history:Annotated[List[int], operator.concat]


def increment(state: ComplexState) -> ComplexState:
    """
    Increment the count in the state by 1 and update sum and history.
    
    Args:
        state (ComplexState): The current state.
    
    Returns:
        ComplexState: The updated state with incremented count, updated sum, and history.
    """
    print(f"Current count: {state['count']}, Sum: {state['sum']}, History: {state['history']}")

    new_count = state['count'] + 1
    return {
        'count': new_count,
        'sum': new_count,
        'history': [new_count]
    }

def should_continue(state: ComplexState):
    """
    Check if the count in the state is less than 10.
    
    Args:
        state (ComplexState): The current state.
    
    Returns:
        str: "continue" if count is less than 10, "end" otherwise.
    """
    if state['count'] < 10:
        print(f"Current count: {state['count']}, Sum: {state['sum']}, History: {state['history']}")
        return "continue"
    else:
        print(f"Final count reached: {state['count']}, Final sum: {state['sum']}, History: {state['history']}")
        return "end"
    

# Define the state graph
graph = StateGraph(ComplexState)

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
        'count': 0,
        'sum': 0,
        'history': []
    }
    response = app.invoke(init_state)
    print("Final state:", response)
    print("State graph execution completed.")   