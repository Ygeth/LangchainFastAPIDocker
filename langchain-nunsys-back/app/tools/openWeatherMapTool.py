import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)
tools = load_tools(["openweathermap-api"], llm)

agent_chain = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)