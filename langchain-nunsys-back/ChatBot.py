import json
import asyncio
import collections
import os
from dotenv import load_dotenv, find_dotenv
from vectorstoreController import VectorstoreController
from typing import List
# from LlmController import LangchainLlms
from ChatOpenAI import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    Document,
    BaseMessage
)
from agentController import AgentController
from langchain.agents import initialize_agent, AgentType

class ChatBot:
  def __init__(self):
    # Initial Prompt
    systemPrompt = f"Eres el asistente para entrevistas de Ricardo, que quiere ser contratado con Ingeniero de LLMs"
    self.__systemPrompt = SystemMessage(content=systemPrompt)

    self.__llm = ChatOpenAI()

  def getLlm(self):
    return self.__llm
  
  # Metodo principal de chat
  def chat(self, *, userQuery: str, cancelToken=None):
    # Use RAG
    (results, history) = vecController.query(userQuery)
    
    print(f"Respuesta: {results["answer"]}")
    print("History:")
    for message in history.messages:
      if isinstance(message, AIMessage):
          prefix = "AI"
      else:
          prefix = "User"

      print(f"{prefix}: {message.content}\n")


  async def test_chatbot(self):
    while True:
      query = input("enter your query: ")
      if query.lower() == "exit":
        return

      self.chat(userQuery=query)

      print("\n")
      print("*" * 100)
      print("\n")

if __name__ == '__main__':
    print("__________ LAUNCH ChatBot ________")
  
    # Load .env variables
    load_dotenv(dotenv_path=find_dotenv())
    print("OPENAI_API key: ", os.environ.get("OPENAI_API_KEY"))
    
    bot = ChatBot()
    vecController = VectorstoreController(bot.getLlm())
    vecController.loadAllDocs()
    
    ## RagChain
    # ragChain = vecController.getRagChain()
    # response = ragChain.invoke({"input": "Quien es kvothe?"})
    
    ## Conversational RagChain
    conversational_rag_chain = vecController.getConversationalRagChain()
    response1 = conversational_rag_chain.invoke({"input": "De que trata la prueba tecnica?"},config={"configurable": {"session_id": "abc123"}})
    print("1, ", response1['answer'])
    response2 = conversational_rag_chain.invoke({"input": "Cual es el quinto punto de la prueba?"},config={"configurable": {"session_id": "abc123"}})
    print("2", response2['answer'])
    
    ## Tools
    agentController = AgentController(bot.getLlm())
    
    # # Agent
    # agent = agentController.getAgent()
    # query = "Que tiempo hará en europa?"
    # config = {"configurable": {"thread_id": "abc123"}}
    # # resp = agent.invoke({"chat_history": [HumanMessage(content=query)]}, config=config)
    # resp = agent.invoke({"chat_history": [HumanMessage(content=query)],})
    # print(resp)
    # print("----")
    
    # Conversational Agent
    # convAgent = agentController.getConversationalAgent()
    # query = "Hola, Soy Ricardo y vivo en Paterna"
    # query2 = "Dime quien soy y el tiempo que hace en mi casa"
    
    # config = {"configurable": {"thread_id": "abc123"}}
    # result = convAgent.invoke(
    #     {"chat_history": [HumanMessage(query)]},
    #     {"configurable": {"session_id": "unused"}},
    # )
    # print(result)
    # tools = load_tools(["openweathermap-api"], bot.getLlm())
    # weather_agent = initialize_agent(tools=tools, llm=bot.getLlm(), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True )

    # weather_agent.run("Que tiempo haré en Valencia mañana?")

    
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(bot.test_chatbot())