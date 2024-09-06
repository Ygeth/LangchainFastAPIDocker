# from pydantic import validator, Extra
from langchain_openai import ChatOpenAI
# https://python.langchain.com/v0.2/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html

# class OpenAI(ChatOpenAI):

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)