# main.py
import argparse
from agents.agent_rag.rag_agent import run_rag
from agents.agent_analysis.analytics_agent import run_analytics
from agents.agent_web.web_agent import run_web
from agents.agent_coordination.coordinator_agent import run_coordinator
from ui.gradio_ui import launch_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="full_pipeline",
                        help="Choose: rag_test | analytics_test | websearch_test | full_pipeline | web_ui")
    args = parser.parse_args()

    if args.mode == "rag_test":
        print(run_rag("What was NVIDIA’s revenue in Q4 2023?"))

    elif args.mode == "analytics_test":
        print(run_analytics("Forecast Microsoft stock for Q3 2025"))

    elif args.mode == "websearch_test":
        print(run_web("Recent Apple stock news"))

    elif args.mode == "full_pipeline":
        while True:
            query = input("\n❓ Enter your query (or 'exit'): ")
            if query.lower() in ["exit", "quit"]:
                break
            result = run_coordinator(query)
            print(result)

    elif args.mode == "web_ui":
        launch_app()

    else:
        print("❌ Invalid mode. Use --help for options.")
