def run_analytics(query):
     return f"[Analytics Agent] Analysieren der Abfrage: {query}"

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

class AnalysisAgent:
    def __init__(self, data_path="./data_outputs/financial_metrics_extracted.csv"):
        self.data_path = data_path
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data not found: {data_path}")
        self.df = pd.read_csv(data_path)
        self._prepare_data()

    def _prepare_data(self):
        self.df["year"] = pd.to_numeric(self.df["year"], errors="coerce")
        self.df["value"] = pd.to_numeric(self.df["value"], errors="coerce")
        self.df = self.df.dropna(subset=["year", "value"])

    def get_metric_timeseries(self, company, metric):
        df_filtered = self.df[
            (self.df["company"].str.lower() == company.lower()) &
            (self.df["metric"].str.lower() == metric.lower())
        ]
        df_grouped = df_filtered.groupby("year")["value"].sum().reset_index()
        df_grouped.rename(columns={"year": "ds", "value": "y"}, inplace=True)
        df_grouped["ds"] = pd.to_datetime(df_grouped["ds"], format="%Y")
        return df_grouped

    def forecast(self, company, metric, years=3):
        df_ts = self.get_metric_timeseries(company, metric)
        if df_ts.shape[0] < 3:
            return {"error": "Not enough historical data for forecasting."}

        model = Prophet(yearly_seasonality=False)
        model.fit(df_ts)
        future = model.make_future_dataframe(periods=years, freq="YE")
        forecast = model.predict(future)
        return {"forecast": forecast, "model": model, "historical": df_ts}

    def plot_forecast(self, model, forecast, company, metric):
        fig = model.plot(forecast)
        plt.title(f"{metric.title()} Forecast for {company.title()}")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.tight_layout()

        # Convert to base64 string for UI or response
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        encoded_img = base64.b64encode(buffer.read()).decode("utf-8")
        plt.close()
        return encoded_img

    def handle_query(self, company, metric, years=3):
        result = self.forecast(company, metric, years)
        if "error" in result:
            return result

        forecast = result["forecast"]
        model = result["model"]
        historical = result["historical"]

        chart = self.plot_forecast(model, forecast, company, metric)
        latest = historical["y"].iloc[-1]
        next_val = forecast.iloc[-1]["yhat"]

        summary = (
            f"{metric.title()} for {company.title()} was approximately {latest:,.0f} "
            f"in {historical['ds'].dt.year.iloc[-1]}. "
            f"The forecast for {forecast['ds'].dt.year.iloc[-1]} is around {next_val:,.0f}."
        )

        return {
            "summary": summary,
            "chart_base64": chart
        }
