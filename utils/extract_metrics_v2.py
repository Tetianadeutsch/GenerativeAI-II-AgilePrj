import os
import re
import glob
import pandas as pd

# Extended keyword dictionary for metrics
TARGET_METRICS = {
    "revenue": [
        r"\brevenue\b", r"net sales", r"total revenue", r"sales", r"turnover",
        r"product revenue", r"services revenue"
    ],
    "operating_income": [
        r"operating income", r"income from operations", r"operating profit",
        r"operating loss", r"loss from operations", r"\bopinc\b"
    ],
    "net_income": [
        r"net income", r"net earnings", r"profit after tax", r"net profit",
        r"consolidated net income", r"net income attributable", r"\bni\b"
    ],
    "eps": [
        r"earnings per share", r"\beps\b", r"diluted earnings per share",
        r"basic earnings per share", r"diluted eps"
    ],
    "total_assets": [
        r"total assets", r"assets total", r"consolidated assets", r"total current assets"
    ],
    "total_liabilities": [
        r"total liabilities", r"liabilities total", r"consolidated liabilities", r"total current liabilities"
    ]
}

def extract_numeric_value(text):
    match = re.search(r'[-+]?\(?\d[\d,.\s\(\)]*\)?', str(text))
    if match:
        raw = match.group(0)
        raw = raw.replace(",", "").replace("(", "-").replace(")", "").strip()
        try:
            return float(raw)
        except:
            return None
    return None

def identify_metric(text):
    text = str(text).lower()
    for metric, patterns in TARGET_METRICS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return metric
    return None

def has_numeric_nearby(text, keyword):
    """Check if a keyword is near a number in the string."""
    pattern = rf"{keyword}.{{0,30}}[-+]?\(?\d[\d,.\s\(\)]*\)?|[-+]?\(?\d[\d,.\s\(\)]*\)?.{{0,30}}{keyword}"
    return re.search(pattern, text.lower()) is not None

def extract_metrics_from_file(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty or df.shape[1] < 2:
            return []

        results = []

        # ROW SEARCH
        for _, row in df.iterrows():
            row_str = " ".join([str(x) for x in row if pd.notnull(x)]).lower()
            for metric, patterns in TARGET_METRICS.items():
                for pattern in patterns:
                    if re.search(pattern, row_str) and has_numeric_nearby(row_str, pattern):
                        value = extract_numeric_value(row_str)
                        if value is not None:
                            results.append((metric, value, "row"))
                            break  # Stop after first matching metric

        # COLUMN HEADER SEARCH
        for col in df.columns:
            col_text = str(col).lower()
            metric = identify_metric(col_text)
            if metric:
                for val in df[col]:
                    num = extract_numeric_value(val)
                    if num is not None:
                        results.append((metric, num, "column"))
                        break

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
    print("\n📊 Extracted Metrics (preview):")
    print(df_metrics.head(20).to_string(index=False))

    output_folder = "./data_outputs"
    os.makedirs(output_folder, exist_ok=True)
    out_path = os.path.join(output_folder, "financial_metrics_extracted.csv")
    df_metrics.to_csv(out_path, index=False)
    print(f"\n💾 Saved extracted metrics to: {out_path}")
