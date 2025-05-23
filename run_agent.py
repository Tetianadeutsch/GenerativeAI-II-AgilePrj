from agents.agent_analysis.analysis_langchain_agent import agent_executor

query1 = "Forecast Meta's revenue for the next 2 years"
query2 = "Compare net income in 2023 across all companies"

response1 = agent_executor.invoke({"input": query1})
print("\n🔮 Forecast Response:\n", response1)

response2 = agent_executor.invoke({"input": query2})
print("\n📊 Comparison Response:\n", response2)
