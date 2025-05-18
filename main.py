# main.py
from agents.agent_rag.rag_agent import run_rag
from agents.agent_analysis.analytics_agent import run_analytics
from agents.agent_web.web_agent import run_web
from agents.agent_coordination.coordinator_agent import run_coordinator
from ui.gradio_ui import launch_app

def menu():
    print("\n📌 Select operation mode:")
    print("1. Test RAG agent")
    print("2. Test Analytics agent")
    print("3. Test Web Search agent")
    print("4. Run full pipeline")
    print("5. Launch web UI (Gradio)")
    print("0. Exit")
    return input("Enter mode number: ").strip()

if __name__ == "__main__":
    while True:
        choice = menu()

        if choice == "1":
            print(run_rag("What was NVIDIA’s revenue in Q4 2023?"))

        elif choice == "2":
            print(run_analytics("Forecast Microsoft stock for Q3 2025"))

        elif choice == "3":
            print(run_web("Recent Apple stock news"))

        elif choice == "4":
            while True:
                query = input("\n❓ Enter your query (or type 'exit'): ")
                if query.lower() in ["exit", "quit"]:
                    break
                result = run_coordinator(query)
                print(result)

        elif choice == "5":
            launch_app()

        elif choice == "0":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid input. Please choose between 0 and 5.")
