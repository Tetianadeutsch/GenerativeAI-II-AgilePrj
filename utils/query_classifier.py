
from utils.call_llm import call_llm

def classify_query(query: str):
    prompt = f"""
You are a smart query classifier.
Given the user query below, determine which agents are required to answer.

Available agents:
- RAG: for investor documents (PDFs, slides, earnings calls)
- Web: for recent news and market sentiment
- Analytics: for analysis, trends, forecasting and visualization

Query: "{query}"
Return the list of agents needed (e.g., RAG, Web, Analytics).
Answer:"""
    response = call_llm(prompt)
    agents = []
    if "rag" in response.lower():
        agents.append("RAG")
    if "web" in response.lower():
        agents.append("Web")
    if "analytics" in response.lower():
        agents.append("Analytics")
    return agents
