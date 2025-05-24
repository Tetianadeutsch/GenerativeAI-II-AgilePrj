# 🤖 Multimodales Marktanalyse-Agentensystem

Dies ist ein generatives Multiagenten-KI-System zur Finanzanalyse. Es kombiniert dokumentenbasiertes Retrieval (RAG), Prognosemodelle und Echtzeit-Marktdaten. Das System wurde mit LangGraph, LangChain und Google Gemini (mit Hugging Face als Fallback) aufgebaut und verarbeitet reale Investor-Relations-Dokumente (IR) von Apple, Google, Meta, Microsoft und NVIDIA (2020–2024).

## 🚀 Funktionen

* **IR-Dokumentensuche (RAG)** mit Quellangaben
* **Finanzprognosen und Trendanalysen** mit Prophet
* **Echtzeit-Nachrichten & Aktienpreise** über Tavily API
* **Modulares Multiagenten-System** mit zentralem Koordinator-Agent
* **Gradio-UI** für benutzerfreundliche Eingabe und Visualisierung

---

## 📂 Projektstruktur

```bash
FINAL_Multi_Agent/
├── app_gradio.py              # Gradio-Oberfläche (Startpunkt)
├── requirements.txt
├── README.md
│
├── agents/
│   ├── agent_rag.py          # Dokumentenagent (RAG)
│   ├── agent_analysis.py     # Prognosen und Vergleiche (Prophet)
│   ├── agent_web.py          # Echtzeitdaten (Tavily)
│   └── coordinator_agent.py  # Koordinations-Agent (Supervisor)
│
├── utils/
│   ├── llm_utils.py          # Auswahl von Gemini / HuggingFace
│   └── data_loader.py        # CSV-Erzeugung aus IR-Daten
│
├── data/                     # IR-Dokumente (PDFs)
├── chroma_db/                # Vektor-Datenbank für RAG
├── data_outputs/             # Verarbeitete CSV-Dateien
```

---

## 🔧 Agentenübersicht

### ✨ RAG-Agent (`agent_rag.py`)

* **Tools**: `search_ir_docs`, `list_sources`
* **Zweck**: Durchsucht IR-Dokumente über Chroma Vektorsuche

### ⚖️ Analyse-Agent (`agent_analysis.py`)

* **Tools**: `forecast_metric`, `compare_metric`
* **Zweck**: Erstellt Finanzprognosen und Vergleiche mit Prophet & Matplotlib

### 📈 Web-Agent (`agent_web.py`)

* **Tools**: `get_stock_price`, `get_market_news`
* **Zweck**: Holt Live-Marktdaten über Tavily-API (mit Fallback)

### 🤖 Koordinator-Agent (`coordinator_agent.py`)

* **Rolle**: Leitet Nutzerfragen an passende Agenten und Tools weiter
* **Tool-Aufrufe**: `route_to_rag`, `route_to_analysis`, `route_to_web`

---

## 📊 Datenaufbereitung

Alle Finanzkennzahlen werden über `utils/data_loader.py` erzeugt. Das Skript liest IR-Dokumente aus und erstellt:

* `financial_metrics_extracted.csv` in `data_outputs/`
* Chroma Vektor-Datenbank wird bei Bedarf automatisch erstellt

---

## ⚙️ Setup & Start

```bash
# Umgebung erstellen (optional mit conda)
conda create -n market-agent python=3.10
conda activate market-agent

# Abhängigkeiten installieren
pip install -r requirements.txt

# Lokalen Start ausführen
python app_gradio.py
```

---

## 🚧 Deployment (Hugging Face Spaces)

* App basiert auf `gr.Blocks()`
* `matplotlib.use("Agg")` ist gesetzt für Headless-Betrieb
* Diagramme werden direkt in der Gradio-Oberfläche angezeigt

---

## 📅 Datengrundlage

* Alle Dokumente stammen von offiziellen Investor-Relations-Seiten von:

  * Apple, Microsoft, Google, NVIDIA, Meta
  * Jahresberichte, Quartalszahlen, Präsentationen (2020–2024)

---

## 🙌 Mitwirkende

Dieses Projekt wurde von einem studentischen Team im Rahmen des Generative AI Agile Project (Sommer 2025) entwickelt. Die Commit-Historie dokumentiert den Fortschritt. Das Projekt entspricht den akademischen Richtlinien.

---

## 🎓 Lizenz

MIT-Lizenz (ausschließlich für Bildungszwecke).
