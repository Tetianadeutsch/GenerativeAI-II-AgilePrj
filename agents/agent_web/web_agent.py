# web_agent_modular/web_agent.py

from typing import List
from clients.tavily_client import search_tavily
from clients.newsapi_client import search_newsapi
from clients.serpapi_client import search_serpapi

def run_web(query: str) -> str:
    print(f"[Web Agent] 🔎 Searching for: {query}\n")

    results: List[str] = []

    # Tavily search
    try:
        tavily_results = search_tavily(query)
        if tavily_results:
            results.append("🔹 Tavily Results:\n" + tavily_results)
    except Exception as e:
        results.append(f"❗ Tavily Error: {e}")

    # NewsAPI search
    try:
        newsapi_results = search_newsapi(query)
        if newsapi_results:
            results.append("🔹 NewsAPI Results:\n" + newsapi_results)
    except Exception as e:
        results.append(f"❗ NewsAPI Error: {e}")

    # SerpAPI search
    try:
        serpapi_results = search_serpapi(query)
        if serpapi_results:
            results.append("🔹 SerpAPI Results:\n" + serpapi_results)
    except Exception as e:
        results.append(f"❗ SerpAPI Error: {e}")

    if not results:
        return "❌ No results from any news source."

    return "\n\n".join(results)

