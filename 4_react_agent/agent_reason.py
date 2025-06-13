from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_react_agent
import datetime
from langchain_community.tools import TavilySearchResults
from langchain import hub

@tool
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time



tavily_search = TavilySearchResults(search_depth="basic")

react_prompt = hub.pull("hwchase17/react")

tools = [tavily_search, get_current_time]

llm = ChatOpenAI(temperature=0)

agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)