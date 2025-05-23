import os
from newsapi import NewsApiClient

# Получение API-ключа из переменных окружения
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")

def search_newsapi(query: str, max_results: int = 5) -> str:
    if not NEWSAPI_API_KEY:
        raise ValueError("❗ NEWSAPI_API_KEY не найден в переменных окружения.")

    # Инициализация клиента
    newsapi = NewsApiClient(api_key=NEWSAPI_API_KEY)

    # Запрос к эндпоинту /v2/everything
    response = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='publishedAt',
        page_size=max_results
    )

    articles = response.get('articles', [])
    if not articles:
        return "❌ Нет новостей от NewsAPI."

    output = ""
    for article in articles:
        title = article.get('title', 'Без заголовка')
        url = article.get('url', 'Нет ссылки')
        output += f"📰 {title}\n🔗 {url}\n\n"

    return output.strip()

