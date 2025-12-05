# utils/vector_store.py

# Updated import for modern LangChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import Tuple
from dotenv import load_dotenv
import os

load_dotenv()  
openai_key = os.getenv("OPENAI_API_KEY")

def embed_and_store(text: str) -> Tuple[FAISS, list]:
    """
    Splits text into chunks, embeds them, and stores them in a FAISS vector store.
    
    Returns:
        - vectorstore: the FAISS vector DB
        - chunks: original text chunks (for debug)
    """
    # 1. Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    
    # 2. Embed chunks
 
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    
    return vectorstore, chunks
