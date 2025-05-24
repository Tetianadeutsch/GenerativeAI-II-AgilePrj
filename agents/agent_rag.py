import os
#from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub

from utils.llm_utils import get_llm  # ✅ Refactored import

# === Tool 1: Search in Chroma DB ===
@tool
def search_ir_docs(query: str) -> str:
    """Searches IR documents for relevant content."""
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")  # <-- Fixed!
    )
    docs = db.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])

# === Tool 2:  ===
@tool
def list_sources(company: str) -> str:
    """List all PDF IR files for the given company."""
    base_path = os.path.join("data", company.lower())
    if not os.path.exists(base_path):
        return f"No data found for {company}."
    files = [f for f in os.listdir(base_path) if f.endswith(".pdf")]
    return "\n".join(files) if files else "No PDFs found."

# === Agent Setup ===
rag_agent = create_react_agent(
    model=get_llm(),
    tools=[search_ir_docs, list_sources],
    prompt=(
        "You are a specialized financial analyst agent.\n"
        "You answer strictly based on investor relations (IR) documents from the last 5 years.\n"
        "Use tools as needed to answer user queries.\n"
        "Provide clear and concise answers based only on the data."
    ),
    name="rag_agent"
)

# === Run example ===
if __name__ == "__main__":
    query = "What are the key revenue highlights for Nvidia in 2024?"
    print("🔍 Query:", query)
    result = rag_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    print("\n📊 Agent response:\n", result)
