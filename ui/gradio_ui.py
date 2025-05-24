<<<<<<< HEAD
# ui/gradio_ui.py

def launch_app():
    print("🔧 Gradio UI is not yet implemented.")
=======
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv

# Подгрузка переменных окружения
load_dotenv()

import gradio as gr
from agents.agent_coordination.coordinator_agent import CoordinatorAgent
from agents.agent_web.web_agent import WebAgent
from agents.agent_analysis.analytics_agent import AnalyticsAgent
from agents.agent_rag.rag_agent import RAGAgent

# Инициализация агентов
web_agent = WebAgent()
analytics_agent = AnalyticsAgent()
rag_agent = RAGAgent()
coordinator = CoordinatorAgent(rag_agent, analytics_agent, web_agent)

# === LangSmith Tracing ===
@traceable(name="ForecastAgentRun")
def run_agent_with_logging(user_input: str):
    return agent_executor.invoke({"input": user_input})

def analyze_query(user_query):
    try:
        responses = coordinator.run(user_query)
        final_answer = responses.get("final_answer", "🤖 No final answer generated.")
        web_response = responses.get("Web", "🌐 No web response.")
        analytics_response = responses.get("Analytics", "📊 No analytics response.")
        rag_response = responses.get("RAG", "📄 No RAG response.")
    except Exception as e:
        final_answer = f"❌ Ошибка: {str(e)}"
        web_response = analytics_response = rag_response = "Ошибка"
    return final_answer, web_response, analytics_response, rag_response

with gr.Blocks(title="📊 Multimodal Market Analyst AI") as demo:
    gr.Markdown("# 🧠 Multimodal Market Analyst")
    gr.Markdown("Enter your financial or market-related query and let the AI agents handle it.")

    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(label="Your query", placeholder="E.g., 'What's the latest on NVIDIA's stock performance?'")
            submit_btn = gr.Button("Analyze")

        with gr.Column():
            final_output = gr.Textbox(label="🧠 Final Aggregated Answer")

    with gr.Accordion("🌐 Web Agent Response", open=False):
        web_output = gr.Textbox(label="Web Search")

    with gr.Accordion("📊 Analytics Agent Response", open=False):
        analytics_output = gr.Textbox(label="Analytics")

    with gr.Accordion("📄 RAG Agent Response", open=False):
        rag_output = gr.Textbox(label="RAG")

    submit_btn.click(fn=analyze_query, inputs=[query_input],
                     outputs=[final_output, web_output, analytics_output, rag_output])

if __name__ == "__main__":
    demo.launch()
>>>>>>> 6b6466847f005bb7417765725469022295c35743
