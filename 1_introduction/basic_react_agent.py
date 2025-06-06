from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, tool
from langchain_community.tools import TavilySearchResults
from datetime import datetime

load_dotenv()

model = ChatOpenAI()



tavily_search = TavilySearchResults(search_depth="basic")
 
tools = [tavily_search]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=True  # Set this to True
)

response = agent.invoke( "when was the IPL final match played in 2025? Calculate the number of days from today." )


print(response["output"])

@tool
def get_current_system_time(format="%Y-%m-%d %H:%M:%S"):
    """Get the current system time in the specified format."""
    return datetime.now().strftime(format)


