from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma(
    collection_name="financial_reports",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

docs = vector_store.similarity_search("show me all documents", k=5)
for doc in docs:
    print(doc.page_content[:500])  # посмотри начало текста
    print(doc.metadata)