# clients/tavily_client.py

import os
import requests

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_tavily(query: str) -> str:
    print(f"[Tavily] Searching: {query}")
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_raw_content": False,
        "max_results": 5
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        return ""

    output = ""
    for item in results:
        title = item.get("title", "No Title")
        link = item.get("url", "No URL")
        output += f"📰 {title}\n🔗 {link}\n\n"

    return output.strip()

