from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_community.tools.openweathermap import openweathermap
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain.agents import AgentType, initialize_agent
from langchain.tools.retriever import create_retriever_tool


# With LangGraph
class AgentController:
  def __init__(self, llm, ragRetriever):
    self.llm = llm
    self.ragRetriever = ragRetriever
    self.tools:list = self.initTools()
    self.memory = MemorySaver()
    
    # self.agent = None
  
  def getAgent(self):
    # if self.agent is None:    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            MessagesPlaceholder("intermediate_steps"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    # agentTool = create_tool_calling_agent(self.llm, self.tools, prompt)
    # agent = AgentExecutor(agent=agentTool, tools=self.tools, verbose=True)
    agent = initialize_agent(tools=self.tools, llm=self.llm, verbose=True)
    return agent
  
  def getConversationalAgent(self, systemPrompt):
    # https://python.langchain.com/v0.2/docs/how_to/chatbots_tools/
    history_for_chain = ChatMessageHistory()
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder("messages"),
            # MessagesPlaceholder("intermediate_steps"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    # agent = create_tool_calling_agent(self.llm, self.tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    # return agent_executor
    conversational_agent_executor = create_react_agent(self.llm, self.tools, checkpointer=self.memory)

    # conversational_agent_executor = RunnableWithMessageHistory(
    #   agent_executor,
    #   lambda session_id: history_for_chain,
    #   input_messages_key="messages",
    #   output_messages_key="output",
    # )
    return conversational_agent_executor
    
  def initTools(self) -> list:
    # https://python.langchain.com/v0.2/docs/integrations/tools/
    tools = load_tools(["openweathermap-api"], self.llm)

    print(self.ragRetriever)
    # Rag Tool
    ragTool = create_retriever_tool(
        self.ragRetriever,
        "ragRetriever",
        "Searches and returns excerpts from the documents attached.",
    )
    
    tools.append(ragTool)
    return tools
    # weather_agent = initialize_agent(tools=tools, llm=bot.getLlm(), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True )