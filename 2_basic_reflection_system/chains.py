from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv


load_dotenv()


generate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a stand up comedian. You will be given a topic and you will generate a joke about it. If user provides a crtitical feedback, you will reflect on it and improve your joke."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflect_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a crtic who provides feedback on jokes. You will be given a joke and you will provide critical feedback on it. If the joke is good, you will say so. If it is bad, you will provide constructive feedback to improve it."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI()

generate_chain = generate_prompt | llm 
reflect_chain = reflect_prompt | llm