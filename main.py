import sys
import os
from dotenv import load_dotenv

# Подгрузка переменных окружения
load_dotenv()

# Добавление корня проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath("utils"))

# Импорт агентов
from agents.agent_rag.rag_agent import RAGAgent
from agents.agent_analysis.analytics_agent import AnalyticsAgent
from agents.agent_web.web_agent import WebAgent
from agents.agent_coordination.coordinator_agent import CoordinatorAgent
from ui.gradio_ui import launch_app


def show_menu():
    print("\n📌 Select operation mode:")
    print("1. 🔍 Test RAG agent")
    print("2. 📊 Test Analytics agent")
    print("3. 🌐 Test Web Search agent")
    print("4. 🤖 Run full pipeline (Coordinator)")
    print("5. 🖥️ Launch web UI (Gradio)")
    print("0. ❌ Exit")


def main():
    rag_agent = RAGAgent()
    analytics_agent = AnalyticsAgent()
    web_agent = WebAgent()
    coordinator = CoordinatorAgent(rag_agent, analytics_agent, web_agent)

    while True:
        show_menu()
        choice = input("Enter mode number: ").strip()

        if choice == "1":
            query = input("🔎 Enter RAG query: ")
            print(rag_agent.run(query))

        elif choice == "2":
            query = input("📈 Enter Analytics query: ")
            print(analytics_agent.run(query))

        elif choice == "3":
            query = input("🌐 Enter Web Search query: ")
            print(web_agent.run(query))

        elif choice == "4":
            while True:
                query = input("\n🤖 Enter your complex query for Coordinator (or 'exit'): ")
                if query.lower() in ["exit", "quit"]:
                    break
                result = coordinator.run(query)
                print("\n🧠 Coordinator Agent Result:\n")
                print(result)

        elif choice == "5":
            print("🖥️ Launching Gradio app.")
            launch_app()

        elif choice == "0":
            print("👋 Exiting.")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
