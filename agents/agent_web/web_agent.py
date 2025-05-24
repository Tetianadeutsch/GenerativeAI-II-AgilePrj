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