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
    self.__llm = ChatOpenAI()
    self.vecController = VectorstoreController(self.__llm)
    self.agentController = AgentController(self.__llm, self.vecController.getRetriever())


  def getLlm(self):
    return self.__llm
  
  # Metodo principal de chat
  def chatConvAgent(self, *, session_id, userQuery: str):
    config = {"configurable": {"thread_id": session_id}}
    systemPrompt = '''Eres el asistente para entrevistas con Nunsys de Ricardo residente en Valencia, 
                      Dispones de varias herramientas, puedes consultar archivos cargados en tu sistema y consultar la metereologia
                      Los archivos son documentos de Ricardo, como sus certificaciones o su curriculum. 
                      Con tus respuestas debes conseguir que contraten a Ricardo en Nunsys para el puesto de Desarrollador de LLM.'''
    convAgent = self.agentController.getConversationalAgent(systemPrompt)
    
    resp = None
    for chunk in convAgent.stream({"messages": [SystemMessage(systemPrompt), HumanMessage(content=userQuery)]}, config):
      print(chunk)
      print("----")
      resp = chunk
    
    return resp
    
  
  # TEST ZONE, Test of RAG, tools, agents...
  ## Metodo de testeo para 
  def chatTest(self, *, userQuery: str):    
    config = {"configurable": {"thread_id": "abc123"}}
    systemPrompt = "Eres el asistente para entrevistas de Ricardo residente en Valencia, puedes buscar en los documentos y consultar el tiempo."
    convAgent = agentController.getConversationalAgent(systemPrompt)
    for chunk in convAgent.stream({"messages": [SystemMessage(systemPrompt), HumanMessage(content=userQuery)]}, config):
      print(chunk)
      print("----")
      
    # print(f"Respuesta: {results["answer"]}")
    # print("History:")
    # for message in convAgent.messages:
    #   if isinstance(message, AIMessage):
    #       prefix = "AI"
    #   else:
    #       prefix = "User"

    #   print(f"{prefix}: {message.content}\n")

  def chatRAG(self, *, session_id, userQuery: str):
    # Use RAG
    (results, history) = self.vecController.query(userQuery)
    print(f"Respuesta: {results["answer"]}")
    return results
  
  def chatAgentTools(self, *, session_id, userQuery: str):
    agent = agentController.getAgent()
    config = {"configurable": {"thread_id": session_id}}
    # query = "Que tiempo hará mañana en Valencia?"
    resp = agent.invoke({
        "chat_history": [SystemMessage(content=systemPrompt)],
        "input": HumanMessage(content=userQuery)
      }, config=config)
    
    return resp

    
  async def test_chatbot(self):
    while True:
      print("___________")
      query = input("Enter your query: ")
      if query.lower() == "exit":
        return

      self.chatTest(userQuery=query)

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
    # Initial Load Docs
    vecController.loadAllDocs()
    
    ## RagChain
    # ragChain = vecController.getRagChain()
    # response = ragChain.invoke({"input": "Quien es kvothe?"})
    
    ## Conversational RagChain
    # conversational_rag_chain = vecController.getConversationalRagChain()
    # response1 = conversational_rag_chain.invoke({"input": "De que trata la prueba tecnica?"},config={"configurable": {"session_id": "abc123"}})
    # print("1, ", response1['answer'])
    # response2 = conversational_rag_chain.invoke({"input": "Que hay que hacer con la memoria del contexto?"},config={"configurable": {"session_id": "abc123"}})
    # print("2", response2['answer'])
    
    ## Tools
    agentController = AgentController(bot.getLlm(), vecController.getRetriever())
    systemPrompt = "Eres el asistente para entrevistas de Ricardo residente en Valencia, que quiere ser contratado con Ingeniero de LLMs, puedes extraer informacion de documentos y del tiempo, pero no tienes porque hacerlo"
    
    ## Agent
    # agent = agentController.getAgent()
    config = {"configurable": {"thread_id": "abc123"}}
    # query = "Que tiempo hará mañana en Valencia?"
    # resp = agent.invoke({
    #     "chat_history": [SystemMessage(content=systemPrompt)],
    #     "input": HumanMessage(content=query)
    #   }, config=config)
    # print("----")
    # print(resp)
    
    ## Conversational Agent
    # convAgent = agentController.getConversationalAgent()
    # query = "Hola, Soy Ricardo y vivo en Valencia"
    # query2 = "Dime quien soy y el tiempo que hace en mi casa"
    # queryRag = "Que hay que hacer en la prueba tecnica"
    # config2 = {"configurable": {"session_id": "abc123"}}
    
    # for chunk in convAgent.stream({"messages": [
    #     SystemMessage(content=systemPrompt),
    #     HumanMessage(content=query)]
    #   }, config):
    #   print(chunk)
    #   print("----")
      
    # for chunk in convAgent.stream({"messages": [HumanMessage(content="Como me llamo? ")]}, config):
    #   print(chunk)
    #   print("----")
    
    # for chunk in convAgent.stream({"messages": [HumanMessage(content="Que tiempo hace donde vivo? ")]}, config):
    #   print(chunk)
    #   print("----")
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.test_chatbot())