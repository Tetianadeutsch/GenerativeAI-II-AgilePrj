<<<<<<< HEAD
# -*- coding: utf-8 -*-# ============ IMPORTS ============
=======
# -*- coding: utf-8 -*-# ============ IMPORTS ============ 
# edit 21.05.2025 by tet.sydorenko - creating csv-files for analysis
>>>>>>> 6b6466847f005bb7417765725469022295c35743
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

<<<<<<< HEAD
=======
import chromadb  # for creating chromadb 
from chromadb.config import Settings

>>>>>>> 6b6466847f005bb7417765725469022295c35743

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
<<<<<<< HEAD
=======
    Examples:
        "Apple_Q1_2023_Report.pdf" ➜ ('apple', '2023', 'quarterly', 'Q1')
>>>>>>> 6b6466847f005bb7417765725469022295c35743
    """
    normalized = normalize_text(filename)
    return (
        next((c for c in ['apple','google','meta','microsoft','nvidia'] if c in normalized), None),
        next((y for y in map(str, range(2019,2025)) if y in filename), None),
        'quarterly' if any(q in normalized for q in ['q1','q2','q3','q4','10q']) else 'annual',
        next((f'Q{i}' for i in range(1,5) if f'q{i}' in normalized), None)
    )

<<<<<<< HEAD
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
=======
# ============ LOAD FROM PICKLE ============
def load_from_pickle(file_path):
    if os.path.exists(file_path):
        logger.info(f"📦 Loading data from {file_path}")
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None


# ============ PROCESS PDFs ============ edit by tet.sydorenko: tables were extracted incorrectly

def create_data_from_pdfs(data_dir="./data", file_path="extracted_documents.pkl"):
    logger.info("⏳ Creating new data from PDFs...")
    extracted_data = []

    for root, _, files in os.walk(data_dir):
        for filename in tqdm(files, desc="Processing files"):
            if is_pdf_file(filename):
                meta = extract_metadata(filename)
                if meta and meta[0]:  # Ensure company name exists
                    try:
                        with pdfplumber.open(os.path.join(root, filename)) as pdf:
                            tables = []
                            for page in pdf.pages:
                                raw_tables = page.extract_tables()
                                for table in raw_tables:
                                    if len(table) > 1 and all(len(row) == len(table[0]) for row in table):  # tet.syd: Checking Column Equality
                                        try:
                                            df = pd.DataFrame(table[1:], columns=table[0])
                                            df.dropna(how="all", inplace=True)
                                            df = df.loc[:, ~df.columns.duplicated()]  # tet.syd: Remove duplicate titles
                                            if df.shape[1] >= 2:  # tet.syd: Let's make sure there are at least 2 columns
                                                tables.append(df)
                                        except Exception as e:
                                            logger.warning(f"⚠️ Error converting table: {e}")

                            if tables:
                                extracted_data.append({
>>>>>>> 6b6466847f005bb7417765725469022295c35743
                                    'company': meta[0],
                                    'file': filename,
                                    'year': meta[1],
                                    'report_type': meta[2],
                                    'quarter': meta[3],
                                    'tables': tables
                                })
                    except Exception as e:
<<<<<<< HEAD
                        logger.error(f"Error processing {filename}: {e}")
        
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    
    with open(file_path, 'rb') as f:
        return pickle.load(f)
=======
                        logger.error(f"❌ Error processing {filename}: {e}")
        
    # Save data to pickle file
    with open(file_path, 'wb') as f:
        pickle.dump(extracted_data, f)
    logger.info(f"✅ Saved {len(extracted_data)} documents to {file_path}")
    return extracted_data

# ============ MAIN FUNCTION ============

def load_data(file_path="extracted_documents.pkl", data_dir="./data"):
    """
    Load data from pickle file if available, otherwise process PDFs and create the file
    """
    extracted_data = load_from_pickle(file_path)
    if extracted_data is None:
        extracted_data = create_data_from_pdfs(data_dir, file_path)
    return extracted_data
>>>>>>> 6b6466847f005bb7417765725469022295c35743

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
<<<<<<< HEAD
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

=======
def create_documents(extracted_data, overwrite_csv: bool = False): # edit by tetsydorenko: export to csv
    """
    Create LangChain documents from relevant financial tables and export them to CSV files.

    Args:
        extracted_data (list): List of dictionaries containing company metadata and raw tables
        overwrite_csv (bool): If True, existing CSV files will be overwritten
    """
    from langchain_core.documents import Document
    import numpy as np
    import re

    documents = []
    os.makedirs("processed_tables", exist_ok=True)  # Ensure target directory exists

    for entry in extracted_data:
        # Build document-level metadata text
        content = f"📊 {entry['company']} {entry['year']} {entry['report_type']}"
        content += f" {entry['quarter']}" if entry['quarter'] else ""
        content += f" from {entry['file']}:\n"

        tables_content = []
        kept_tables = 0

        for i, df in enumerate(entry['tables']):
            # Remove empty rows and columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            if df.empty or df.shape[1] < 2:
                continue

            try:
                # Attempt to convert potential financial strings to numeric values
                numeric_candidate = df.apply(lambda col: col.map(
                    lambda x: float(str(x).replace(",", "").replace("$", "").replace("€", "").strip())
                    if isinstance(x, str) and re.search(r"\d", x)
                    else np.nan
                ))

                numeric_cols = numeric_candidate.dropna(axis=1, thresh=3)
                valid_rows = numeric_candidate.dropna(how='all')

                # Keep only tables with at least 2 numeric columns and 3 valid rows
                if numeric_cols.shape[1] < 2 or valid_rows.shape[0] < 3:
                    logger.info(f"ℹ️ Table {i} from {entry['file']} skipped: not enough numeric content.")
                    continue

                # === Save CSV ===
                filename_parts = [
                    entry['company'],
                    entry['year'] or "unknown",
                    entry['quarter'] or "annual",
                    f"table{i}"
                ]
                csv_filename = f"./processed_tables/{'_'.join(filename_parts)}.csv"

                if overwrite_csv or not os.path.exists(csv_filename):
                    df.to_csv(csv_filename, index=False)
                    logger.info(f"💾 Saved: {csv_filename}")
                else:
                    logger.info(f"🛑 Skipped existing file: {csv_filename}")

                # Add to document content
                tables_content.append(f"\n--- Table {i} ---\n{df.to_markdown(index=False)}")
                kept_tables += 1

            except ValueError as e:
                if "could not convert string to float" in str(e):
                    logger.info(f"ℹ️ Table {i} from {entry['file']} skipped: non-numeric or malformed content.")
                else:
                    logger.warning(f"⚠️ Unexpected error in table {i} from {entry['file']}: {e}")
            except Exception as e:
                logger.warning(f"⚠️ General error in table {i} from {entry['file']}: {e}")


        # Finalize and save the LangChain document if valid tables were found
>>>>>>> 6b6466847f005bb7417765725469022295c35743
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
<<<<<<< HEAD
    
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
=======

    logger.info("✅ Created %d relevant documents", len(documents))
    return documents



# ============ VECTOR STORE ============
def initialize_vector_store():
    """
    Initialize Chroma vector database using PersistentClient
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
       
    persist_directory = "./chroma_db" # pass for saving chromadb
    print('\nPERSISTANT DIRECTORY: ',persist_directory)
    chroma_client = chromadb.PersistentClient(path=persist_directory) # create PersistentClient!

    return Chroma(
        client=chroma_client,
        collection_name="financial_reports",
        embedding_function=embeddings,
        persist_directory=persist_directory
>>>>>>> 6b6466847f005bb7417765725469022295c35743
    )

# ============ MAIN PROCESS ============
def main():
    try:
        # 1. Load data
        data = load_data()
        
        # 2. Create documents
<<<<<<< HEAD
        documents = create_documents(data)
=======
        documents = create_documents(data,overwrite_csv=True) # REMOVE overwrite_csv=True (should be False!)
>>>>>>> 6b6466847f005bb7417765725469022295c35743
        
        # 3. Initialize vector store
        vector_store = initialize_vector_store()
        
<<<<<<< HEAD
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
=======
        # 4. Store documents in batches (edit by tet.sydorenko: Store documents only if collection is empty)
        collection_size = vector_store._collection.count()
        logger.info("📦 Existing documents in vector DB: %d", collection_size)

        if collection_size == 0:
            batch_size = 5000
            total_docs = len(documents)
            logger.info("⏳ Storing %d documents in batches of %d", total_docs, batch_size)

            for batch_start in range(0, total_docs, batch_size):
                batch = documents[batch_start:batch_start + batch_size]
                vector_store.add_documents(batch)
                batch_num = (batch_start // batch_size) + 1
                logger.info("✅ Batch %d with %d documents added", batch_num, len(batch))
        else:
            logger.info("✅ Vector store already contains documents. Skipping insertion.")
              
        # 5. Example search
        query = "What was Meta's net income in 2023?"
>>>>>>> 6b6466847f005bb7417765725469022295c35743
        logger.info("🔍 Searching for: %s", query)
        
        results = vector_store.similarity_search(query, k=3)
        for i, doc in enumerate(results, 1):
            logger.info("\n🔎 Result %d:\n%.300s...\n📎 Metadata: %s", 
                       i, doc.page_content, doc.metadata)
<<<<<<< HEAD
=======

        # Save ChromaDB
        logger.info("💾 ChromaDB persisted at ./chroma_db")
>>>>>>> 6b6466847f005bb7417765725469022295c35743
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()