# agents/agent_rag/rag_agent.py

class RAGAgent:
    def run(self, query: str) -> dict:
        return {
            "agent_name": "RAGAgent",
            "result": f"📄 RAGAgent: Dummy response for query: '{query}'",
            "sources": ["https://example.com/fake_rag_source"]
        }

