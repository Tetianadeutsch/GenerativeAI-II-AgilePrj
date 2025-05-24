# 🤖 Multimodal Market Intelligence Agent

This is a multi-agent generative AI system for financial analytics, combining document-based search (RAG), market forecasting, and real-time stocknews updates. The project is built with LangGraph, LangChain, and Google Gemini (with Hugging Face fallback), and processes real-world Investor Relations (IR) documents from Apple, Google, Meta, Microsoft, and NVIDIA (2020–2024).

## 🚀 Features

 IR document search (RAG) with citations
 Forecasting & trend analysis using Prophet
 Real-time news & stock data via Tavily
 Modular multi-agent system coordinated by a Supervisor agent
 Gradio-based UI for easy user interaction

---

## 📂 Project Structure

```bash
FINAL_Multi_Agent
├── app_gradio.py              # Gradio interface entry point
├── requirements.txt
├── README.md
│
├── agents
│   ├── agent_rag.py          # Document-based agent with RAG tools
│   ├── agent_analysis.py     # Forecasting and comparison (Prophet)
│   ├── agent_web.py          # Real-time info (Tavilynews)
│   └── coordinator_agent.py  # Supervisor agent that routes tasks
│
├── utils
│   ├── llm_utils.py          # LLM selector with GeminiHuggingFace fallback
│   └── data_loader.py        # Loads and formats financial CSV data
│
├── data                     # Raw IR PDF documents
├── chroma_db                # Vector DB for RAG (auto-generated)
├── data_outputs             # Processed CSV files (e.g., metrics)
```

---

## 🔧 Agent Overview

### ✨ RAG Agent (`agent_rag.py`)

 Tools `search_ir_docs`, `list_sources`
 Goal Search through IR documents (PDFs) using Chroma vector search.

### ⚖️ Analysis Agent (`agent_analysis.py`)

 Tools `forecast_metric`, `compare_metric`
 Goal Create forecasts and comparisons using Prophet and Matplotlib.

### 📈 Web Agent (`agent_web.py`)

 Tools `get_stock_price`, `get_market_news`
 Goal Fetch live data using Tavily API and fallback logic.

### 🤖 Coordinator Agent (`coordinator_agent.py`)

 Role Receives the user's question, routes to the right agenttool.
 Tool calls `route_to_rag`, `route_to_analysis`, `route_to_web`

---

## 📊 Data Preparation

All financial metrics are extracted using `utilsdata_loader.py`.
This script processes IR documents and outputs

 `financial_metrics_extracted.csv` in `data_outputs`
 Chroma DB is generated automatically if missing.

---

## ⚙️ Setup & Run

```bash
# Create environment (if using conda)
conda create -n market-agent python=3.10
conda activate market-agent

# Install dependencies
pip install -r requirements.txt

# Run locally
python app_gradio.py
```

---

## 🚧 Deployment (Hugging Face Spaces)

 App built with `gr.Blocks()`
 `matplotlib.use(Agg)` is enforced for headless image rendering
 Charts are displayed in the Gradio UI when available

---

## 📅 Dataset

 All documents sourced from official IR pages of

   Apple, Microsoft, Google, NVIDIA, Meta
   Annual reports, Q-earnings slides, investor decks (2020–2024)

---

## 🙌 Credits

This project was developed by a student team as part of the Generative AI Agile Project (Summer 2025). Commit history documents team progress. Project complies with ethical and academic guidelines.
   - Head: Hussam Alafandi
   
   - Team members:

        - Rahaf – RAG Agent

        - Tetiana Sydorenko – Data Science & Forecasting  

        - Vadim Filatov – Real-Time Data Integration


---

## 🎓 License

MIT License (for educational purposes only).
