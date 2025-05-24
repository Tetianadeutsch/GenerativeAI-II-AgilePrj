import os
import datetime
import yfinance as yf
#from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub
import requests
from bs4 import BeautifulSoup

from utils.llm_utils import get_llm  # ✅ Refactored import

# === TOOL 1: Get Latest News ===
@tool
def get_latest_news(company: str) -> str:
    """Fetch the latest news headlines about a company (Google News + fallback)."""
    # Primary source: Google News
    query = company.replace(" ", "+")
    url = f"https://news.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article h3")[:3]
        if articles:
            headlines = [a.get_text() for a in articles]
            return "\n".join(f"- {h}" for h in headlines)
    except Exception as e:
        print("⚠️ Google News error:", e)

    # Fallback: Bing News RSS
    try:
        rss_url = f"https://www.bing.com/news/search?q={query}&format=RSS"
        rss_response = requests.get(rss_url, headers=headers, timeout=10)
        rss_soup = BeautifulSoup(rss_response.content, features="xml")
        items = rss_soup.find_all("item")[:3]
        if items:
            headlines = [item.title.get_text() for item in items]
            return "\n".join(f"- {h}" for h in headlines)
    except Exception as e:
        print("⚠️ Bing News fallback error:", e)

    return "❌ Sorry, no recent news could be found for that company."


# === TOOL 2: Get Stock Price ===
@tool
def get_stock_price(company: str) -> str:
    """Retrieves current stock price and last close for a public company."""
    print(f"📈 Fetching stock data for: {company}")
    symbol_map = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "meta": "META",
        "facebook": "META",
        "nvidia": "NVDA",
    }
    symbol = symbol_map.get(company.lower())
    if not symbol:
        return f"❌ No symbol found for {company}."
    data = yf.Ticker(symbol).history(period="1d")
    if data.empty:
        return f"❌ No stock data found for {symbol}."
    current = data["Close"].iloc[-1]
    date = data.index[-1].strftime("%Y-%m-%d")
    return f"💹 {company.title()} stock price on {date}: ${current:.2f}"

# === Agent ===
web_agent = create_react_agent(
    model=get_llm(),
    tools=[get_latest_news, get_stock_price],
    prompt=(
        "You are a web intelligence agent focused on financial updates and market trends. "
        "You can retrieve current stock prices and summarize the latest financial news. "
        "Use your tools and answer directly based on the most recent information."
    ),
    name="web_agent"
)

# === Example usage ===
if __name__ == "__main__":
    query = "What are the latest financial headlines and stock price for Google?"
    print("\n🔍 Query:", query)
    response = web_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("\n📰 Result:\n", response)
