def run_coordinator(query):
    # Здесь может быть вызов других агентов (позже добавим)
    return f"[Coordinator Agent] Koordinierte Antwort auf: {query}"

from agents.agent_analysis.analytics_agent import AnalysisAgent

class CoordinatorAgent:
    def __init__(self):
        self.analysis_agent = AnalysisAgent()

    def handle_query(self, query: str):
        query = query.lower()

        if "forecast" in query or "predict" in query:
            return self._delegate_to_analysis(query)
        else:
            return {"response": "This query is not handled yet by the coordinator."}

    def _delegate_to_analysis(self, query: str):
        # Simple heuristic: extract company and metric
        import re
        companies = ["apple", "meta", "google", "nvidia", "microsoft"]
        metrics = ["revenue", "net income", "eps", "operating income"]

        company = next((c for c in companies if c in query), None)
        metric = next((m for m in metrics if m in query), None)

        match = re.search(r"(\d+) year", query)
        forecast_years = int(match.group(1)) if match else 3

        if not company or not metric:
            return {"error": "Could not identify company or metric in the query."}

        result = self.analysis_agent.handle_query(company, metric, years=forecast_years)

        return result
