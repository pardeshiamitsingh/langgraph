from dotenv import load_dotenv
from agent_reason import agent_runnable, tools
from agent_state import AgentState

load_dotenv()

def reason_node(state: AgentState) -> AgentState:
    """
    Reasoning node for the agent.
    
    Args:
        state (AgentState): The current state of the agent.
    
    Returns:
        AgentState: The updated state after reasoning.
    """
    print(f"Agent is reasoning about the question: {state['input']}")
    print(f"Agent is reasoning about the question: {state['intermediate_steps']}")
    agent_output = agent_runnable.invoke(state)

    print(f"agent_outp######: {agent_output}")

    return {
        'agent_response': agent_output
    }


def act_node(state: AgentState) -> AgentState:
    """
    Action node for the agent.
    
    Args:
        state (AgentState): The current state of the agent.
    
    Returns:
        AgentState: The updated state after performing the action.
    """
    agent_action = state['agent_response']

    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    print(f"Agent is performing action: {tool_name} with input: {tool_input}")

    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break

    if tool_function:
        if isinstance(tool_input, dict):
            
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)

    else:
        output = f"Tool '{tool_name}' not found"

    print(f"Agent output after tool execution {output} with input: {tool_input}")


    return {"intermediate_steps": [(agent_action, str(output))]}