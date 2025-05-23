import os
import pandas as pd
from dotenv import load_dotenv
from prophet import Prophet
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
import gradio as gr
from PIL import Image  # Добавлен импорт для отображения картинок
from langsmith import traceable

from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub

# === Load environment variables ===
load_dotenv()

# === Select LLM ===
def get_llm():
    if os.getenv("GOOGLE_API_KEY"):
        print("✅ Using Gemini Flash")
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    elif os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        print("⚠️ Using HuggingFace fallback")
        return HuggingFaceHub(
            repo_id="google/flan-t5-base",
            model_kwargs={"temperature": 0.3, "max_length": 512}
        )
    else:
        raise EnvironmentError("❌ No API key found in .env")

# === Load data ===
DATA_PATH = "./data_outputs/financial_metrics_extracted.csv"
df = pd.read_csv(DATA_PATH)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["year", "value"])

# === TOOL 1: Forecast ===
@tool
def analyze_metric(company: str, metric: str, years: int = 3, period: str = "annual") -> dict:
    """Forecast a financial metric for a company by year or quarter and return summary + chart."""
    print(f"📌 analyze_metric called with company={company}, metric={metric}, years={years}, period={period}")
    company = company.lower()
    metric = metric.lower()
    period = period.lower().strip()
    if any(x in period for x in ["quarter", "quartal"]):
        period = "quarterly"
    elif any(x in period for x in ["year", "annual"]):
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

    freq = "QE" if period == "quarterly" else "Y"
    future = model.make_future_dataframe(periods=years * (4 if period == "quarterly" else 1), freq=freq)
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

        # define next N year after origin data
        last_year = df_prophet["ds"].dt.year.max()
        future_years = forecast_by_year[forecast_by_year["year"] >= last_year + 1].head(years)


        for _, row in future_years.iterrows():
            summary += f"- {int(row['year'])}: {row['yhat']:,.2f}\n"

        # forecast["year"] = forecast["ds"].dt.year
        # forecast_by_year = forecast.groupby("year")["yhat"].mean().reset_index()
        # last_year = df_prophet["ds"].dt.year.max()
        # future_years = forecast_by_year[forecast_by_year["year"] > last_year]
        # for _, row in future_years.iterrows():
        #     summary += f"- {int(row['year'])}: {row['yhat']:,.2f}\n"

    return {"summary": summary, "chart_base64": chart_base64}

# === TOOL 2: Compare ===
@tool
def compare_metric(metric: str, year: int) -> dict:
    """Compare a financial metric across companies for a given year and return summary + chart."""
    print(f"📌 compare_metric called with metric={metric}, year={year}")
    filtered = df[
        (df["metric"].str.lower() == metric.lower()) &
        (df["year"] == year)
    ]
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

# === Prompt ===
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful financial analyst AI. Always call the appropriate tool (analyze_metric or compare_metric) to answer the user's query. Do not generate responses on your own."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# === Agent setup ===
llm = get_llm()
tools = [analyze_metric, compare_metric]
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# === LangSmith Tracing ===
@traceable(name="ForecastAgentRun")
def run_agent_with_logging(user_input: str):
    return agent_executor.invoke({"input": user_input})

# === Gradio Interface ===
def gradio_interface(user_input):
    try:
        response = run_agent_with_logging(user_input)
        output_text = response["output"].get("summary", response["output"]) if isinstance(response["output"], dict) else response["output"]
        img = None
        if isinstance(response["output"], dict) and response["output"].get("chart_base64"):
            try:
                image_bytes = base64.b64decode(response["output"]["chart_base64"])
                img = Image.open(BytesIO(image_bytes))
            except Exception as e:
                output_text += f"\n⚠️ Could not decode image: {e}"
        return output_text, img
    except Exception as e:
        return f"❌ Error: {str(e)}", None

with gr.Blocks() as demo:
    gr.Markdown("### 📊 Financial Agent Interface")
    input_text = gr.Textbox(label="Enter your request")
    output_text = gr.Textbox(label="Summary")
    output_image = gr.Image(label="Chart")
    submit_btn = gr.Button("Run Agent")

    submit_btn.click(fn=gradio_interface, inputs=[input_text], outputs=[output_text, output_image])

if __name__ == "__main__":
    demo.launch()
