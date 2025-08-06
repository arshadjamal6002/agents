# utils/qa_chain.py

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain.vectorstores.base import VectorStore
import os 
from dotenv import load_dotenv
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def build_qa_chain(vectorstore: VectorStore) -> RetrievalQA:
    """
    Creates a LangChain RetrievalQA chain using an OpenAI LLM and a vector retriever.
    """
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)
    
    llm = OpenAI(
        temperature=0.2,
        model_name="gpt-3.5-turbo-instruct",  # fast + low cost
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
    
    return qa_chain
