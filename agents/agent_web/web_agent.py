<<<<<<< HEAD
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

=======
from clients.tavily_client import search_tavily

class WebAgent:
    def run(self, query: str) -> dict:
        try:
            search_result = search_tavily(query)
            results = search_result.get("results", [])[:3]

            if not results:
                return {
                    "agent_name": "WebAgent",
                    "result": "🌐 No relevant results found.",
                    "sources": []
                }

            summary_lines = []
            sources = []

            for r in results:
                title = r.get("title", "No Title")
                url = r.get("url", "")
                summary_lines.append(f"- [{title}]({url})")
                if url:
                    sources.append(url)

            summary = "\n".join(summary_lines)

            return {
                "agent_name": "WebAgent",
                "result": f"🌐 WebAgent Results:\n{summary}",
                "sources": sources
            }

        except Exception as e:
            return {
                "agent_name": "WebAgent",
                "result": f"❌ Error during web search: {e}",
                "sources": []
            }
>>>>>>> 6b6466847f005bb7417765725469022295c35743
