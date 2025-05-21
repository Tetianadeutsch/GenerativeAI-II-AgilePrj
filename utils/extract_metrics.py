import os
import re
import glob
import pandas as pd

# Extended synonyms for better coverage
TARGET_METRICS = {
    "revenue": ["revenue", "net sales", "total revenue", "sales", "turnover"],
    "operating_income": ["operating income", "income from operations", "operating profit"],
    "net_income": ["net income", "net earnings", "profit after tax"],
    "eps": ["earnings per share", "eps", "diluted earnings per share"],
    "total_assets": ["total assets", "assets total", "total company assets"],
    "total_liabilities": ["total liabilities", "liabilities total"]
}

def extract_numeric_value(text):
    match = re.search(r'[-+]?\$?\(?\d[\d,.\(\)\s]*\)?', str(text))
    if match:
        raw = match.group(0)
        raw = raw.replace("$", "").replace(",", "").replace("(", "-").replace(")", "").strip()
        try:
            return float(raw)
        except:
            return None
    return None

def identify_metric(text):
    text = str(text).lower()
    for metric, keywords in TARGET_METRICS.items():
        if any(k in text for k in keywords):
            return metric
    return None

def extract_metrics_from_file(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty or df.shape[1] < 2:
            return []

        results = []

        # Check rows
        for _, row in df.iterrows():
            row_text = " ".join([str(x) for x in row if pd.notnull(x)])
            metric = identify_metric(row_text)
            if metric:
                value = extract_numeric_value(row_text)
                if value is not None:
                    results.append((metric, value, "row"))

        # Check column headers
        for col in df.columns:
            metric = identify_metric(col)
            if metric:
                # Try to get the first numeric value in the column
                for val in df[col]:
                    num = extract_numeric_value(val)
                    if num is not None:
                        results.append((metric, num, "column"))
                        break  # take only first found value

        return results
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

def extract_all_metrics(folder="./processed_tables"):
    files = glob.glob(os.path.join(folder, "*.csv"))
    extracted = []

    for file_path in files:
        file_name = os.path.basename(file_path)
        parts = file_name.split("_")
        company = parts[0]
        year = parts[1] if len(parts) > 1 else "unknown"
        quarter = parts[2] if len(parts) > 2 else "annual"

        rows = extract_metrics_from_file(file_path)
        for metric, value, source in rows:
            extracted.append({
                "company": company,
                "year": year,
                "quarter": quarter,
                "file": file_name,
                "metric": metric,
                "value": value,
                "source": source
            })

    return pd.DataFrame(extracted)

if __name__ == "__main__":
    df_metrics = extract_all_metrics()
    print("\n📊 Extracted Metrics:")
    print(df_metrics.head(20).to_string(index=False))

    output_folder = "./data_outputs"
    os.makedirs(output_folder, exist_ok=True)
    df_metrics.to_csv(os.path.join(output_folder, "financial_metrics_extracted.csv"), index=False)
    print(f"\n💾 Saved extracted metrics to {output_folder}/financial_metrics_extracted.csv")
