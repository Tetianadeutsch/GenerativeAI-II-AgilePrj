import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Config for plots
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

DATA_PATH = "./data_outputs/financial_metrics_extracted.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    return df

def preprocess(df):
    # Ensure year is numeric
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year", "value"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"])

def plot_metric_trend(df, company, metric):
    df_filtered = df[(df["company"] == company) & (df["metric"] == metric)]
    if df_filtered.empty:
        print(f"No data for {company} - {metric}")
        return

    df_grouped = df_filtered.groupby("year")["value"].sum().reset_index()

    #plt.figure()
    sns.lineplot(data=df_grouped, x="year", y="value", marker="o")
    plt.title(f"{metric.title()} Trend for {company.title()}")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()

def plot_company_comparison(df, metric, year=None):
    df_filtered = df[df["metric"] == metric]
    if year:
        df_filtered = df_filtered[df_filtered["year"] == year]
    if df_filtered.empty:
        print(f"No data for {metric} in {year if year else 'all years'}")
        return

    df_grouped = df_filtered.groupby("company")["value"].sum().reset_index()

    #plt.figure()
    sns.barplot(data=df_grouped, x="company", y="value")
    plt.title(f"{metric.title()} Comparison by Company" + (f" ({year})" if year else ""))
    plt.xlabel("Company")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)

    # Examples: metrics: net_income | eps | total_assets | operating_income | revenue

    plot_metric_trend(df, company="apple", metric="eps")
    plot_metric_trend(df, company="google", metric="net_income")

    plot_company_comparison(df, metric="revenue", year=2023)
    plot_company_comparison(df, metric="net_income", year=2020)

    plot_company_comparison(df, metric="net_income")  # без фильтра по году
    print(df[df["metric"] == "net_income"].groupby(["company", "year"]).size())

