import json
import asyncio
import collections
import os
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname

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

class ChatBot:
  def __init__(self):
    # Initial Prompt
    systemPrompt = f"Eres el asistente para entrevistas de Ricardo, que quiere ser contratado con Ingeniero de LLMs"
    self.__systemPrompt = SystemMessage(content=systemPrompt)

    # VectorStore
    self.__memory = FAISS(
      embedding_function= OpenAIEmbeddings(),
      index=IndexFlatL2,
      docstore=InMemoryDocstore({}),
      index_to_docstore_id={}
    )
    
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
      # async for token, _ in self.chat(userQuery=query):
      #   print(token, end='')

      print("\n")
      print("*" * 100)
      print("\n")

if __name__ == '__main__':
    # Load .env variables
    load_dotenv(find_dotenv)
    SECRET_KEY = os.environ.get("OPENAI_API_KEY")

    print("OPENAI_API key: ", SECRET_KEY)
    
    # bot = ChatBot()
    # vecController = VectorstoreController(bot.getLlm())
    # vecController.loadAllDocs()
    
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(bot.test_chatbot())