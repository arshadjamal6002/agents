# agents/doc_qa_agent/tool.py

from utils.pdf_reader import extract_text_from_pdf
from utils.vector_store import embed_and_store
from utils.qa_chain import build_qa_chain

def tool(input: dict) -> dict:
    """
    ADK tool function interface.
    
    Input:
        {
            "pdf_path": "path/to/file.pdf",
            "question": "What is the main clause?"
        }

    Output:
        {
            "answer": "The main clause is ...",
            "sources": ["...chunk text..."]
        }
    """
    pdf_path = input.get("pdf_path")
    question = input.get("question")
    
    if not pdf_path or not question:
        return {"error": "Missing pdf_path or question"}

    try:
        text = extract_text_from_pdf(pdf_path)
        vectorstore, _ = embed_and_store(text)
        qa = build_qa_chain(vectorstore)
        result = qa.invoke({"query": question})
        
        sources = [doc.page_content for doc in result["source_documents"]]

        return {
            "answer": result["result"],
            "sources": sources
        }
    except Exception as e:
        return {"error": str(e)}
