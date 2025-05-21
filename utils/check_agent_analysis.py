import sys
import os

# Make sure parent directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.agent_analysis.analytics_agent import AnalysisAgent

# Set company and metric to test
company = "apple"
metric = "operating_income"
forecast_years = 7

# Initialize agent
agent = AnalysisAgent()

# Debug: check which metrics are available for the company
available_metrics = agent.df[agent.df["company"] == company]["metric"].unique()
print(f"\n🔍 Available metrics for {company.title()}: {available_metrics}")

# Run forecast and response generation
response = agent.handle_query(company, metric, years=forecast_years)

# Print result
if "summary" in response:
    print("\n📊 Summary:")
    print(response["summary"])

    # Optional: save image to file for testing
    with open("forecast_chart.png", "wb") as f:
        import base64
        f.write(base64.b64decode(response["chart_base64"]))
    print("📈 Forecast chart saved as forecast_chart.png")

else:
    print("\n⚠️ Forecast failed:")
    print(response.get("error", "Unknown error"))
