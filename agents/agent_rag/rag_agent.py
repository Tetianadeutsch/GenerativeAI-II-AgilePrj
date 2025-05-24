<<<<<<< HEAD
def run_rag(query):
    return f"[RAG Agent] Antwort auf eine Anfrage: {query}"
=======
# agents/agent_rag/rag_agent.py

class RAGAgent:
    def run(self, query: str) -> dict:
        return {
            "agent_name": "RAGAgent",
            "result": f"📄 RAGAgent: Dummy response for query: '{query}'",
            "sources": ["https://example.com/fake_rag_source"]
        }
>>>>>>> 6b6466847f005bb7417765725469022295c35743

