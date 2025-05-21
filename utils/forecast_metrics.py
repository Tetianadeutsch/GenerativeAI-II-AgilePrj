import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

DATA_PATH = "./data_outputs/financial_metrics_extracted.csv"

def load_and_prepare_data(company, metric):
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing file: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    # Filter by company and metric (case-insensitive)
    df = df[(df["company"] == company.lower()) & (df["metric"] == metric.lower())]
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "value"])

    # Group by year and aggregate values (if duplicates)
    df = df.groupby("year")["value"].sum().reset_index()

    # Prepare for Prophet (ds = datetime, y = target)
    df.rename(columns={"year": "ds", "value": "y"}, inplace=True)
    df["ds"] = pd.to_datetime(df["ds"], format="%Y")
    return df

def forecast_metric(df, periods=3):
    model = Prophet(yearly_seasonality=False)
    model.fit(df)

    # Extend time series into the future
    future = model.make_future_dataframe(periods=periods, freq="YE")
    forecast = model.predict(future)

    return model, forecast

def plot_forecast(model, forecast, company, metric):
    fig = model.plot(forecast)
    plt.title(f"{metric.title()} Forecast for {company.title()}")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Set forecast parameters
    company = "meta"           # <- change to any company name
    metric = "net_income"      # <- change to any metric from dataset
    forecast_years = 7         # <- adjust how many years into the future
    
    # Run forecast
    df = load_and_prepare_data(company, metric)

    if df.shape[0] < 3:
        print(f"⚠️ Not enough data to forecast for {company} - {metric}")
    else:
        model, forecast = forecast_metric(df)
        plot_forecast(model, forecast, company, metric)
