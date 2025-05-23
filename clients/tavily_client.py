import os
import requests

def search_tavily(query: str) -> dict:
    print(f"[Tavily] Searching: {query}")
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")

    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "query": query,
        "search_depth": "basic",
        "include_answers": False,
        "max_results": 5
    }

    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()