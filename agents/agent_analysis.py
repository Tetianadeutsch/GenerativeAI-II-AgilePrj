import os
import matplotlib
matplotlib.use("Agg")  # Avoid GUI issues in headless environments like Gradio
import pandas as pd
#from dotenv import load_dotenv
from prophet import Prophet
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub

from utils.llm_utils import get_llm  # ✅ Refactored import

# === Load dataset ===
DATA_PATH = "data_outputs/financial_metrics_extracted.csv"
df = pd.read_csv(DATA_PATH)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["year", "value"])

# === TOOL 1: Forecast ===
@tool
def analyze_metric(company: str, metric: str, years: int = 3, period: str = "annual") -> dict:
    """Forecast a financial metric for a company by year or quarter and return summary + chart."""
    company = company.lower()
    metric = metric.lower()
    period = period.lower().strip()
    if "quart" in period:
        period = "quarterly"
    else:
        period = "annual"

    if period == "quarterly":
        df_q = df[
            (df["company"].str.lower() == company) &
            (df["metric"].str.lower() == metric) &
            (df["quarter"].notna()) &
            (~df["quarter"].astype(str).str.lower().str.contains("annual"))
        ].copy()

        if df_q.empty:
            return {"summary": f"⚠️ No valid quarterly data for {company.title()} - {metric}"}

        df_q["quarter"] = df_q["quarter"].astype(str).str.extract(r"(\d)").astype(int)
        df_q["year"] = df_q["year"].astype(int)
        df_q["quarter_str"] = df_q["year"].astype(str) + "Q" + df_q["quarter"].astype(str)
        df_q["ds"] = df_q["quarter_str"].apply(lambda x: pd.Period(x, freq="Q").start_time)

        df_prophet = df_q.groupby("ds")["value"].sum().reset_index().rename(columns={"value": "y"})
    else:
        df_y = df[
            (df["company"].str.lower() == company) &
            (df["metric"].str.lower() == metric)
        ].copy()

        if df_y.empty:
            return {"summary": f"⚠️ No valid annual data for {company.title()} - {metric}"}

        df_y["ds"] = pd.to_datetime(df_y["year"].astype(int).astype(str), format="%Y")
        df_prophet = df_y.groupby("ds")["value"].sum().reset_index().rename(columns={"value": "y"})

    model = Prophet(yearly_seasonality=True)
    model.fit(df_prophet)

    freq = "Q" if period == "quarterly" else "Y"
    future = model.make_future_dataframe(periods=years * (4 if freq == "Q" else 1), freq=freq)
    forecast = model.predict(future)

    fig = model.plot(forecast)
    plt.title(f"{metric.title()} Forecast for {company.title()} ({period.title()})")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    chart_base64 = base64.b64encode(buf.getvalue()).decode()

    summary = f"\n📈 {metric.title()} Forecast for {company.title()} ({period.title()}):\n"
    if period == "quarterly":
        last_forecasts = forecast[["ds", "yhat"]].tail(4 * years)
        for _, row in last_forecasts.iterrows():
            quarter = (row["ds"].month - 1) // 3 + 1
            label = f"{row['ds'].year}-Q{quarter}"
            summary += f"- {label}: {row['yhat']:,.2f}\n"
    else:
        forecast["year"] = forecast["ds"].dt.year
        forecast_by_year = forecast.groupby("year")["yhat"].mean().reset_index()
        future_years = forecast_by_year.tail(years)
        for _, row in future_years.iterrows():
            summary += f"- {int(row['year'])}: {row['yhat']:,.2f}\n"

    return {"summary": summary, "chart_base64": chart_base64}

# === TOOL 2: Compare ===
@tool
def compare_metric(metric: str, year: int, companies: str = "") -> dict:
    """
    Compare a financial metric across companies for a given year.
    Optional: provide a comma-separated list of companies to limit comparison.
    """
    filtered = df[
        (df["metric"].str.lower() == metric.lower()) &
        (df["year"] == year)
    ]

    if companies:
        company_list = [c.strip().lower() for c in companies.split(",")]
        filtered = filtered[filtered["company"].str.lower().isin(company_list)]

    if filtered.empty:
        return {"summary": f"❌ No data for {metric} in {year}"}

    summary = f"📊 {metric.title()} in {year}:\n"
    companies = []
    values = []
    for company, val in filtered.groupby("company")["value"].sum().sort_values(ascending=False).items():
        summary += f"- {company.title()}: {val:,.0f}\n"
        companies.append(company.title())
        values.append(val)

    fig, ax = plt.subplots()
    ax.bar(companies, values)
    ax.set_title(f"{metric.title()} in {year}")
    ax.set_ylabel(metric.title())
    ax.set_xlabel("Company")
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    chart_base64 = base64.b64encode(buf.getvalue()).decode()

    return {"summary": summary, "chart_base64": chart_base64}

# === Agent ===
analysis_agent = create_react_agent(
    model=get_llm(),
    tools=[analyze_metric, compare_metric],
    prompt=(
        "You are a data analysis agent specialized in financial trends. "
        "You can perform metric forecasting and comparison using structured financial data. "
        "Use tools as needed and return only the results."
    ),
    name="analysis_agent"
)

if __name__ == "__main__":

    query = "Forecast Apple revenue for 2 years (quarterly) and compare revenue in 2023 for Apple and Meta"
    print("🔍 Query:", query)
    result = analysis_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print("\n📊 Result:\n", result)
