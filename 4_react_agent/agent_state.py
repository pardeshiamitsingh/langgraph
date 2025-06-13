from typing import TypedDict, List, Annotated, Union
from langgraph.graph import START, END, StateGraph
from langchain_core.agents import AgentAction, AgentFinish
import operator


#define the state
class AgentState(TypedDict):
    """
    A state representation for the agent.
    """
    input: str
    agent_response: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[List[tuple[AgentAction, str]], operator.concat]