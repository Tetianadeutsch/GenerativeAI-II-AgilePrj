# -*- coding: utf-8 -*-# ============ IMPORTS ============
import os
import re
import pickle
import logging
import warnings
import pandas as pd
import pdfplumber
import torch
from tqdm import tqdm
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ============ CONFIGURATION ============
warnings.filterwarnings("ignore", message="CropBox missing")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# ============ MODEL INITIALIZATION ============
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
logger.info("⚡ GPU active: %s", torch.cuda.is_available())
logger.info("🖥️ Model device: %s", model.device)

# ============ ENVIRONMENT VARIABLES ============
load_dotenv()
os.environ["LANGSMITH_TRACING"] = "true"
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Multi_Agenten"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# ============ HELPER FUNCTIONS ============
def normalize_text(text):
    """Normalize text by removing special characters"""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def is_pdf_file(filename):
    """Check if file is PDF"""
    return filename.lower().endswith('.pdf')

def extract_metadata(filename):
    """
    Extract company name, year, report type and quarter from filename
    """
    normalized = normalize_text(filename)
    return (
        next((c for c in ['apple','google','meta','microsoft','nvidia'] if c in normalized), None),
        next((y for y in map(str, range(2019,2025)) if y in filename), None),
        'quarterly' if any(q in normalized for q in ['q1','q2','q3','q4','10q']) else 'annual',
        next((f'Q{i}' for i in range(1,5) if f'q{i}' in normalized), None)
    )

# ============ DATA LOADING ============
def load_data(file_path="extracted_documents.pkl"):
    """
    Load data from pickle file or create new one
    """
    if not os.path.exists(file_path):
        logger.info("⏳ Creating new data file...")
        data = []
        
        for root, _, files in os.walk('./data'):
            for filename in tqdm(files, desc="Processing files"):
                if is_pdf_file(filename) and (meta := extract_metadata(filename))[0]:
                    try:
                        with pdfplumber.open(os.path.join(root, filename)) as pdf:
                            tables = [
                                pd.DataFrame(table[1:], columns=table[0]) 
                                for page in pdf.pages 
                                for table in page.extract_tables() 
                                if len(table) > 1
                            ]
                            if tables:
                                data.append({
                                    'company': meta[0],
                                    'file': filename,
                                    'year': meta[1],
                                    'report_type': meta[2],
                                    'quarter': meta[3],
                                    'tables': tables
                                })
                    except Exception as e:
                        logger.error(f"Error processing {filename}: {e}")
        
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# ============ TABLE FILTERING ============
def is_relevant_table(dataframe):
    """
    Check if table contains relevant financial data
    """
    if dataframe is None or dataframe.empty:
        return False

    keywords = ["cash", "assets", "liabilities", "revenue", "income", "total", "net", "equity"]
    banlist = ["item", "management", "controls", "procedures", "legal", "discussion", "risk"]

    try:
        flat_text = " ".join(str(value).lower() for value in dataframe.values.flatten() if pd.notnull(value))
        
        if any(banned in flat_text for banned in banlist):
            return False

        keyword_matches = sum(1 for keyword in keywords if keyword in flat_text)
        return keyword_matches >= 2 or any(currency in flat_text for currency in ["$", "€", "%"])
    except Exception:
        return False

# ============ DOCUMENT CREATION ============
def create_documents(extracted_data):
    """
    Create Langchain documents from relevant tables
    """
    documents = []
    for entry in extracted_data:
        # Create document header
        content = f"📊 {entry['company']} {entry['year']} {entry['report_type']}"
        content += f" {entry['quarter']}" if entry['quarter'] else ""
        content += f" from {entry['file']}:\n"
        
        tables_content = []
        kept_tables = 0
        
        # Process and filter tables
        for i, table_df in enumerate(entry['tables']):
            if not is_relevant_table(table_df):
                continue
            try:
                tables_content.append(f"\n--- Table {i} ---\n{table_df.to_markdown(index=False)}")
                kept_tables += 1
            except Exception as e:
                logger.warning(f"Table conversion error: {e}")
                tables_content.append(f"\n--- Table {i} ---\n{str(table_df)}")
                kept_tables += 1

        if kept_tables > 0:
            content += "\n".join(tables_content)
            documents.append(Document(
                page_content=content,
                metadata={
                    "company": entry['company'],
                    "file": entry['file'],
                    "year": entry['year'],
                    "report_type": entry['report_type'],
                    "quarter": entry['quarter']
                }
            ))
    
    logger.info("✅ Created %d relevant documents", len(documents))
    return documents

# ============ VECTOR STORE ============
def initialize_vector_store():
    """
    Initialize Chroma vector database
    """
    embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return Chroma(
        collection_name="financial_reports",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

# ============ MAIN PROCESS ============
def main():
    try:
        # 1. Load data
        data = load_data()
        
        # 2. Create documents
        documents = create_documents(data)
        
        # 3. Initialize vector store
        vector_store = initialize_vector_store()
        
        # 4. Store documents in batches
        batch_size = 5000
        total_docs = len(documents)
        logger.info("⏳ Storing %d documents in batches of %d", total_docs, batch_size)
        
        for batch_start in range(0, total_docs, batch_size):
            batch = documents[batch_start:batch_start + batch_size]
            vector_store.add_documents(batch)
            batch_num = (batch_start // batch_size) + 1
            logger.info("✅ Batch %d with %d documents added", batch_num, len(batch))
        
        # 5. Example search
        query = "What was Microsoft's net income in 2023?"
        logger.info("🔍 Searching for: %s", query)
        
        results = vector_store.similarity_search(query, k=3)
        for i, doc in enumerate(results, 1):
            logger.info("\n🔎 Result %d:\n%.300s...\n📎 Metadata: %s", 
                       i, doc.page_content, doc.metadata)
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()