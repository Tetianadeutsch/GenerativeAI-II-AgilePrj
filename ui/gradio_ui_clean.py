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
rag_agent = RAGAgent()
analytics_agent = AnalyticsAgent()
web_agent = WebAgent()
coordinator = CoordinatorAgent(rag_agent, analytics_agent, web_agent)

# Функция для анализа запроса
def analyze_query(query):
    try:
        result = coordinator.run(query)
        final_answer = result["final_answer"]
        raw_responses = result["raw_responses"]

        # Форматирование результата
        formatted_answer = ""
        for agent, response in raw_responses.items():
            formatted_answer += f"### 🤖 {response['agent_name']}\n"
            formatted_answer += f"{response['result']}\n\n"
            if response.get("sources"):
                formatted_answer += "**Sources:**\n" + "\n".join(f"- {src}" for src in response["sources"]) + "\n\n"

        return formatted_answer, raw_responses["RAG"]["result"], raw_responses["Analytics"]["result"], raw_responses["Web"]["result"]
    except Exception as e:
        return f"❌ Ошибка: {e}", "", "", ""

# Интерфейс
with gr.Blocks(title="🧠 Multimodal Financial AI System") as demo:
    gr.Markdown("# 📊 Multimodal Financial Analyst\nEnter your market-related question below:")

    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(label="Your query", lines=2, placeholder="e.g., What is Meta's forecast for next quarter?")
            analyze_button = gr.Button("🔍 Analyze")

        with gr.Column():
            final_output = gr.Markdown(label="Final Aggregated Answer")

    with gr.Row():
        rag_output = gr.Textbox(label="📄 RAG Agent", lines=3)
        analytics_output = gr.Textbox(label="📊 Analytics Agent", lines=3)
        web_output = gr.Textbox(label="🌐 Web Agent", lines=3)

    analyze_button.click(fn=analyze_query, inputs=[query_input], outputs=[final_output, rag_output, analytics_output, web_output])

demo.launch()