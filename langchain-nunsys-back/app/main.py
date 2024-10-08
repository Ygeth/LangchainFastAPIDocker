from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os
# Project imports
from ChatBot import ChatBot
from vectorstoreController import VectorstoreController
from agentController import AgentController

# Load .env variables
load_dotenv(dotenv_path=find_dotenv())
print("OPENAI_API key: ", os.environ.get("OPENAI_API_KEY"))

bot = ChatBot()
vecController = VectorstoreController(bot.getLlm())
# agentController = AgentController(bot.getLlm(), vecController.getRetriever())
app = FastAPI()

# Pydantic model
class ChatMsg(BaseModel):
    query: str
    sessionId: str = "nunsys"
    
    
@app.post("/chat")
async def chat(chatMsg: ChatMsg):
    """
    Endpoint to handle chat requests.

    This method receives a chat message and a user session, then sends the user's query
    to the chatbot to generate a response.

    Parameters:
    - chatMsg (ChatMsg): An object containing the user's query (`query`) and session ID (`sessionId`).

    Returns:
    - resp: The response generated by the chatbot based on the user's query.
    """
    try:
        resp = bot.chatConvAgent(userQuery=chatMsg.query, session_id=chatMsg.sessionId)
        return resp
    except Exception as e:
        return {"error": str(e)}


@app.post("/loadDocs")
async def loadDocs():
    """
    Endpoint to load documents into the system.

    This method triggers the `loadAllDocs` function from the vector controller (`vecController`)
    to load all available documents into the system for information processing.

    Returns:
    - None: This endpoint does not return any direct response, it only triggers the document loading process.
    """
    try:
      vecController.loadAllDocs()
      return {"status": "Documents loaded successfully"}
    except Exception as e:
      return {"error": str(e)}

## Otros endpoints para comprobar cada modulo
@app.post("/chatAgentTools")
async def chatAgentTools(chatMsg: ChatMsg):
    try:
        resp = bot.chatAgentTools(userQuery=chatMsg.query, session_id=chatMsg.sessionId)
        return resp
    except Exception as e:
        return {"error": str(e)}

@app.post("/chatRAG")
async def chatRAG(chatMsg: ChatMsg):
    try:
        resp = bot.chatRAG(userQuery=chatMsg.query, session_id=chatMsg.sessionId)
        return resp
    except Exception as e:
        return {"error": str(e)}

