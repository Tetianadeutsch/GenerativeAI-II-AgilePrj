import os
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub

from utils.llm_utils import get_llm  # ✅ Refactored import

# === Load existing agents ===
from agents.agent_rag import rag_agent
from agents.agent_analysis import analysis_agent
from agents.agent_web import web_agent

# === Define routing tools ===
@tool
def route_to_rag(query: str) -> str:
    """Send the query to the RAG Agent."""
    result = rag_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result['messages'][-1].content

@tool
def route_to_analysis(query: str) -> str:
    """Send the query to the Data Analysis Agent."""
    result = analysis_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result['messages'][-1].content

@tool
def route_to_web(query: str) -> str:
    """Send the query to the Web Search Agent."""
    result = web_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result['messages'][-1].content

# === Define Supervisor Agent ===
coordinator_agent = create_react_agent(
    model=get_llm(),
    tools=[route_to_rag, route_to_analysis, route_to_web],
    prompt=(
        "You are the coordinator agent. Your job is to analyze user requests and decide whether to delegate them to one of the specialist agents: \n"
        "- Use `route_to_rag` for document-based questions about past financial data.\n"
        "- Use `route_to_analysis` for forecasts, metrics, and visual comparisons.\n"
        "- Use `route_to_web` for real-time market updates or recent news.\n"
        "Respond only with the tool output."
    ),
    name="coordinator_agent"
)

# === Test ===
if __name__ == "__main__":
    user_query = "Based on the investor reports, what were the main operating_income drivers for Apple in 2023, make operating_income forecast for the next 2 years, and are there any recent news that might affect their stock performance?"
    print("🔍 User query:", user_query)
    result = coordinator_agent.invoke({"messages": [{"role": "user", "content": user_query}]})
    print("\n🤖 Supervisor agent response:\n", result)
