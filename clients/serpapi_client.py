import os
import requests

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

<<<<<<< HEAD
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
=======
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

>>>>>>> 6b6466847f005bb7417765725469022295c35743

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
<<<<<<< HEAD
        results = []

        for item in data.get("organic_results", []):
            title = item.get("title", "No title")
            link = item.get("link", "No URL")
            results.append({"title": title, "url": link})

        return results

    except Exception as e:
        return [{"title": f"❗ Error fetching from SerpAPI: {e}", "url": ""}]
=======

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
>>>>>>> 6b6466847f005bb7417765725469022295c35743
