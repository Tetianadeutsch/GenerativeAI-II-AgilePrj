<<<<<<< HEAD
def run_coordinator(query):
    # Здесь может быть вызов других агентов (позже добавим)
    return f"[Coordinator Agent] Koordinierte Antwort auf: {query}"
=======
# agents/agent_coordination/coordinator_agent.py

from agents.agent_web.web_agent import WebAgent
from agents.agent_rag.rag_agent import RAGAgent
from agents.agent_analysis.analytics_agent import AnalyticsAgent
from utils.call_llm import call_llm
from utils.query_classifier import classify_query
from langsmith import traceable

class CoordinatorAgent:
    def __init__(self, rag_agent, analytics_agent, web_agent):
        self.rag_agent = rag_agent
        self.analytics_agent = analytics_agent
        self.web_agent = web_agent

    def run(self, query: str) -> str:
        print(f"\n🤖 Coordinator: Classifying the query...")
        selected_agents = classify_query(query)
        print(f"🔎 Coordinator: Selected agents: {selected_agents}")

        responses = {}

        if "RAG" in selected_agents and self.rag_agent:
            print(f"📄 Coordinator: Calling RAG Agent...")
            responses["RAG"] = self.rag_agent.run(query)

        if "Analytics" in selected_agents and self.analytics_agent:
            print(f"📊 Coordinator: Calling Analytics Agent...")
            responses["Analytics"] = self.analytics_agent.run(query)

        if "Web" in selected_agents and self.web_agent:
            print(f"🌐 Coordinator: Calling Web Agent...")
            responses["Web"] = self.web_agent.run(query)

        print(f"\n🧠 Coordinator: Aggregating responses...")
        final_answer = self.aggregate_responses(query, responses)

        print(f"\n🧠 Coordinator Agent Result:\n{final_answer}")
        return final_answer

    def aggregate_responses(self, query: str, responses: dict) -> str:
        # Формируем текст для LLM-агрегации
        aggregation_prompt = f"""
You are an intelligent financial assistant helping to summarize and explain insights.

User query: {query}

Below are the responses from different specialized agents:

"""

        for agent, response in responses.items():
            aggregation_prompt += f"\n[{agent}]\n{response['result']}\n"

        aggregation_prompt += """
Please provide a final aggregated answer for the user, combining insights, removing duplication, and adding clarity.
Keep the tone confident, helpful, and brief (2-5 sentences).
Also highlight any trends or contrasts if found.
Answer:"""

        # Получаем ответ от LLM
        try:
            aggregated = call_llm(aggregation_prompt, max_tokens=512)
        except Exception as e:
            aggregated = f"❌ Error during aggregation: {str(e)}"

        return f"📌 Aggregated answer for query: '{query}'\n\n{aggregated}\n\n" + \
               "\n".join([f"[{agent}]\n{resp}" for agent, resp in responses.items()])
>>>>>>> 6b6466847f005bb7417765725469022295c35743
