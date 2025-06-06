
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import TavilySearchResults

load_dotenv()

model = ChatOpenAI()

tavily_search = TavilySearchResults(search_depth="basic")

tools = [tavily_search]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    return_intermediate_steps=True  # Ensure this is set to True
)

# Call the agent using the __call__ method instead of agent.run()
response = agent({"input": "Give me a tweet about todays weather in San Francisco."})

# Access and print the intermediate steps
intermediate_steps = response["intermediate_steps"]
print("Intermediate Steps:", intermediate_steps)

# Access and print the final output
final_answer = response["output"]
print("Final Answer:", final_answer)
