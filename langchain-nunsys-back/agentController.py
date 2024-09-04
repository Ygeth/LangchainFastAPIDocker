from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

# With LangGraph
class AgentController:
  def __init__(self, llm):
    self.llm = llm
    self.tools:list = self.initTools()
    self.memory = MemorySaver()
    self.agent = None
  
  def getAgent(self):
    if self.agent is None:
      prompt = ChatPromptTemplate.from_messages(
          [
              (
                  "system",
                  "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
              ),
                MessagesPlaceholder("chat_history"),
                MessagesPlaceholder("intermediate_steps"),
                MessagesPlaceholder("agent_scratchpad"),
                ("human", "{input}")
          ]
      )
      agentTool = create_tool_calling_agent(self.llm, self.tools, prompt)
      self.agent = AgentExecutor(agent=agentTool, tools=self.tools, verbose=True)
    return self.agent
  
  def getConversationalAgent(self):
    demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

    conversational_agent_executor = RunnableWithMessageHistory(
      self.getAgent(),
      lambda session_id: demo_ephemeral_chat_history_for_chain,
      input_messages_key="chat_history",
      output_messages_key="output",
    )
    return conversational_agent_executor
    
  def initTools(self) -> list:
    tools = load_tools(["openweathermap-api"], self.llm)

    return tools
    # weather_agent = initialize_agent(tools=tools, llm=bot.getLlm(), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True )