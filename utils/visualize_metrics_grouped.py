import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
sns.set(style="whitegrid", palette="deep")
plt.rcParams["figure.figsize"] = (16, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10

DATA_PATH = "./data_outputs/financial_metrics_extracted.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    return df

def preprocess(df):
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year", "value"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"])

def plot_metrics_grouped(df, metrics):
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(8 * n, 6))

    if n == 1:
        axes = [axes]

    for ax, metric in zip(axes, metrics):
        df_metric = df[df["metric"] == metric]
        if df_metric.empty:
            ax.set_title(f"No data for {metric}")
            continue

        df_grouped = df_metric.groupby(["company", "year"])["value"].sum().reset_index()

        sns.lineplot(data=df_grouped, x="year", y="value", hue="company", marker="o", ax=ax)
        ax.set_title(f"{metric.replace('_', ' ').title()} Trend")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)

    # Choose which metrics to display side-by-side # Examples: metrics: net_income | eps | total_assets | operating_income | revenue
    selected_metrics = ["revenue", "net_income"]
    plot_metrics_grouped(df, selected_metrics)
