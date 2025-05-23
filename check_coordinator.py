from agents.agent_coordination.coordinator_agent import CoordinatorAgent

agent = CoordinatorAgent()

query = "Forecast Apple's revenue for 5 years"
response = agent.handle_query(query)

if "summary" in response:
    print("\n✅ Summary:")
    print(response["summary"])
    # Save chart
    with open("coordinator_forecast.png", "wb") as f:
        import base64
        f.write(base64.b64decode(response["chart_base64"]))
else:
    print("\n❌ Error:")
    print(response.get("error", "Unknown"))

if "chart_base64" in response:
    with open("coordinator_forecast.png", "wb") as f:
        import base64
        f.write(base64.b64decode(response["chart_base64"]))
    print("📈 Forecast chart saved as coordinator_forecast.png")
