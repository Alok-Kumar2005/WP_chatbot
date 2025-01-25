from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

def get_llm():
    llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=api_key
)
    

    return llm