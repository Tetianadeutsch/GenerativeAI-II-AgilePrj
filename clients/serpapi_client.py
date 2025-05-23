import os
import requests

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_serpapi(query: str) -> str:
    if not SERPAPI_API_KEY:
        return "❗ SERPAPI_API_KEY not found in environment variables"

    print(f"[SerpAPI] Searching: {query}")
    url = "https://serpapi.com/search.json"
    params = {
    "q": "Apple stock news",
    "tbm": "nws",
    "hl": "en",
    "gl": "us",
    "api_key": SERPAPI_API_KEY,
    "num": 10,  # Пробуем ограничить, но не надеемся на это
    "tbs": "sbd:1"
}


    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        news_results = data.get("news_results", [])
        if not news_results:
            return "❌ No news found from SerpAPI."

        output = ""
        for item in news_results:
            title = item.get("title", "No Title")
            link = item.get("link", "No Link")
            output += f"📰 {title}\n🔗 {link}\n\n"

        return output.strip()

    except Exception as e:
        return f"❗ SerpAPI Error: {e}"
