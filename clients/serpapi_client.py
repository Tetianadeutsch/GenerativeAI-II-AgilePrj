import os
import requests

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_serpapi(query: str, max_results: int = 5) -> list:
    if not SERPAPI_API_KEY:
        raise ValueError("❗ SERPAPI_API_KEY not found in environment variables")

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": max_results,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        results = []

        for item in data.get("organic_results", []):
            title = item.get("title", "No title")
            link = item.get("link", "No URL")
            results.append({"title": title, "url": link})

        return results

    except Exception as e:
        return [{"title": f"❗ Error fetching from SerpAPI: {e}", "url": ""}]
