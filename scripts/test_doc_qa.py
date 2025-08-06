# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.doc_qa_agent.tool import tool

result = tool({
    "pdf_path": "agents/doc_qa_agent/sample_docs/document.pdf",
    "question": "What is the refund policy?"
})

print("🔍 Full result:", result)
# print("📌 Answer:", result["answer"])  # Keep this for now
