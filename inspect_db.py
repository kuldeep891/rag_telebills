import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def inspect_vector_store():
    if not os.path.exists(DB_DIR):
        print(f"Database directory not found at {DB_DIR}")
        return

    print(f"Connecting to ChromaDB at {DB_DIR}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

    # Get all documents
    # Note: Chroma's get() method returns a dict with 'ids', 'embeddings', 'metadatas', 'documents'
    data = vector_store.get()
    
    count = len(data['ids'])
    print(f"\nTotal Documents in Store: {count}")
    
    if count == 0:
        print("Store is empty.")
        return

    print("\n=== Last 3 Documents ===")
    start_index = max(0, count - 3)
    for i in range(start_index, count):
        print(f"\n[Document {i+1}]")
        print(f"ID: {data['ids'][i]}")
        print(f"Source: {data['metadatas'][i].get('source', 'Unknown')}")
        print(f"Page: {data['metadatas'][i].get('page', '?')}")
        print("-" * 40)
        print(f"Content:\n{data['documents'][i]}") # Show full content
        print("-" * 40)

if __name__ == "__main__":
    inspect_vector_store()
