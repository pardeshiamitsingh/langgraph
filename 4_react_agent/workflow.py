from langgraph.graph import START, END, StateGraph
from agent_state import AgentState
from langchain_core.agents import AgentFinish, AgentAction

from dotenv import load_dotenv
from workflow_nodes import reason_node, act_node
graph = StateGraph(AgentState)

ACTION_NODE = "action_node"
REASON_NODE = "reason_node"

def should_continue(state: AgentState):
    """
    Check if the agent has finished its task.
    
    Args:
        state (AgentState): The current state of the agent.
    
    Returns:
        str: "continue" if the agent needs to reason again, "end" otherwise.
    """
    if isinstance(state['agent_response'], AgentFinish):
        print(f"Agent has finished with response: {state['agent_response'].return_values}")
        return  END
    else:
        print(f"Agent is reasoning about the question: {state['input']}")
        return ACTION_NODE

graph.add_node(REASON_NODE, reason_node)
graph.add_node(ACTION_NODE, act_node)

graph.set_entry_point(REASON_NODE)
graph.add_conditional_edges(REASON_NODE, should_continue)
graph.add_edge(ACTION_NODE,REASON_NODE)

app = graph.compile()

result = app.invoke({
    'input': "get the current date and lastest SpaceX launch date and find the difference in days?",
    'agent_response': None,
    'steps': []
})

print(result["agent_response"], "final result")