# GenerativeAI-II-AgilePrj
Final Project: "Multimodal Market Analyst AI System"

📌 Project Summary:
Students will build a multimodal AI system capable of answering market-related queries, providing investment insights, analyzing historical market performance, generating forecasts, and visualizing financial data. The system consists of specialized collaborative agents coordinated by a central agent, using real-world financial data sourced exclusively from Investor Relations (IR) publications (PDF reports, slides, earnings call documents, etc.) for Apple, Microsoft, Google, NVIDIA, and Meta over the past 5 years.

🖥️ System Overview & Agents' Roles
The multi-agent framework includes clearly defined specialized agents:

🌟 1. Multimodal Agentic RAG Specialist
Core Responsibility:

Handle multimodal financial queries (textual questions, financial tables, images/charts, PDFs).
Retrieve relevant financial data specifically from IR documents of Apple, Microsoft, Google, NVIDIA, and Meta (past 5 years).
Provide accurate and cited answers based explicitly on these sources.
Capabilities & Tasks:

Multimodal embeddings generation (CLIP, SentenceTransformers).
Document indexing and retrieval (FAISS, Chroma).
Answer synthesis with explicit citations.
Example User Query:

“Summarize NVIDIA’s recent financial performance based on this earnings presentation.”

Example Output:

“NVIDIA’s Q4 FY24 revenue rose by 18%, driven by strong GPU sales (source: NVIDIA Q4 FY24 Earnings Slides, page 5).”

🌟 2. Data Science & Analytics Agent
Core Responsibility:

Conduct advanced market analytics, trend analyses, and predictive modeling.
Produce forecasts, explanatory insights, and visualizations.
Capabilities & Tasks:

Extract structured data from IR documents (financial tables, earnings data).
Forecasting and predictive modeling (stock-price forecasting with Prophet/ARIMA).
Visualization creation (Matplotlib, Plotly).
Generate explanatory textual insights for analytical findings.
Example User Query:

“Analyze Microsoft’s stock performance over the past year and forecast its performance next quarter.”

Example Output:

Interactive stock-price visualization.
A forecast for the next quarter with clearly presented confidence intervals and explanatory text.
🌟 3. Web Search & Real-Time Market Agent
Core Responsibility:

Retrieve real-time market news, financial events, and current sentiment.
Extract timely information from reputable online financial sources.
Capabilities & Tasks:

Web scraping and real-time data retrieval (Yahoo Finance, Alpha Vantage, NewsAPI).
Summarize recent market sentiment and relevant updates clearly with citations.
Example User Query:

“What's the latest news affecting Google’s stock price today?”

Example Output:

"Google's stock rose 3% today, driven by positive market reactions to its latest AI product announcements (source: CNBC, May 2025)."

🌟 4. Coordinator Agent
Core Responsibility:

Orchestrate complex queries, decompose tasks, and manage agent collaboration.
Aggregate individual agent outputs into coherent, citation-rich summaries.
Capabilities & Tasks:

Task decomposition and delegation (LangChain, GPT-based agents).
Workflow coordination and response integration.
Example Workflow:

Decompose multimodal query:

Retrieval and synthesis (RAG Agent).
Forecast and visualization generation (Data Science Agent).
Real-time sentiment and news retrieval (Web Search Agent).
Aggregate results into unified, cited analysis.

🌟 (Optional) 5. Quality Assurance & Ethical AI Reviewer
Core Responsibility:

Ensure accuracy, reliability, and ethical integrity of generated outputs.
Validate factual correctness and appropriate citations.
Capabilities & Tasks:

Automated moderation, bias checks, and fact verification.
Ensure transparency, fairness, and ethical compliance.
🎨 System Workflow (Example scenario):
User Query (multimodal input):

"Based on these recent charts and current news, summarize Meta’s stock performance and predict its next-quarter outlook."

Coordinator Agent:

Parses query.
Assigns tasks to appropriate agents.
Individual Agents respond:

RAG Agent: Summarizes provided IR documents.
Web Search Agent: Retrieves latest market sentiment/news.
Data Science Agent: Generates stock-price predictions and visualizations.
Coordinator Agent aggregates:

Produces integrated, multimodal financial analysis with citations.
(Optional) QA Agent: Ensures answer quality, citations, and ethical compliance.

Final Result: Presented via a Gradio UI deployed to Hugging Face Spaces.

🛠️ Recommended Technical Stack
Agent	Tools/Models
Agentic RAG Specialist	CLIP, SentenceTransformers, LangChain, FAISS, Chroma, GPT (LoRA fine-tuning optional)
Data Science Agent	Pandas, Matplotlib, Plotly, Prophet, scikit-learn, GPT
Web Search Agent	SerpAPI/NewsAPI, Tavily, BeautifulSoup, newspaper3k, OpenAI/HF API
Coordinator Agent	LangChain Agents framework, GPT (API-based)
QA & Ethical Reviewer Agent	BERT-based classifiers, GPT moderation API, Hugging Face evaluation tools
🎯 Dataset (Explicitly Defined):
Investor Relations documents (2020–2024) for:

Apple, Microsoft, Google, NVIDIA, Meta
Document types:

Annual reports (10-K), quarterly reports (10-Q)
Earnings call transcripts and slides
Investor presentations, charts, graphs
🧑‍💻 Student Workflow (Agile):
Week 1:

Dataset acquisition and preparation from IR resources.
Multimodal document processing and embeddings.
Initial agent implementations.
Full RAG implementation with retrieval and citation.
Analytics agent: forecasting and visualization.
Week 2:

Web search integration, real-time data extraction.
Coordinator agent implementation.
Integration of all agents.
QA agent and ethical validation (optional).
Fine-tuning of RAG and quality assurance agents on the provided dataset (optional).
UI development with Gradio; final deployment.
📦 Final Deliverables:
🚀 Gradio-based Hugging Face Spaces Application
📁 Well-documented GitHub Repository
📊 Jira Project Board (Agile Documentation)
🎬 Presentation & Demo
📑 Technical report (architecture, decisions, reflections)
✅ Why this System?
Students will gain real-world experience directly aligned with professional roles in financial analysis and generative AI, learning:

Advanced multimodal data retrieval
Financial data analysis and visualization
Predictive analytics and forecasting
Web scraping and real-time data integration
Agile teamwork, Jira-based project management
Production-grade deployment skills
This project mirrors the exact type of multimodal AI financial analytics systems currently deployed in industry, significantly enhancing student employability.

Resources
Workflows and Agents
Multi-agent supervisor
Multi-Vector Retriever for RAG on tables, text, and images
How to pass multimodal data to models
Multi-agent systems
Multi-agent supervisor
How to get your RAG application to return sources
How to get a RAG application to add citations
