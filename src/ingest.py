import os
import glob
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.utils import PIIMasker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_pdfs(directory: str) -> List[Document]:
    """Loads all PDF files from the specified directory."""
    documents = []
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {directory}")
        return []

    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(pdf_file)
            docs = loader.load()
            documents.extend(docs)
            logger.info(f"Loaded {len(docs)} pages from {pdf_file}")
        except Exception as e:
            logger.error(f"Error loading {pdf_file}: {e}")
            
    return documents

def mask_pii_in_documents(documents: List[Document]) -> List[Document]:
    """Iterates through documents and masks PII in the page_content."""
    masker = PIIMasker()
    masked_docs = []
    
    for doc in documents:
        # Create a new document to avoid mutating the original in place if that matters
        # though here we just want the result
        original_text = doc.page_content
        masked_text = masker.mask_text(original_text)
        
        # Update metadata to indicate masking
        new_metadata = doc.metadata.copy()
        new_metadata["pii_masked"] = True
        
        masked_doc = Document(page_content=masked_text, metadata=new_metadata)
        masked_docs.append(masked_doc)
        
    return masked_docs

def ingest_data():
    # 1. Load Data
    logger.info("Loading PDFs...")
    raw_documents = load_pdfs(DATA_DIR)
    if not raw_documents:
        logger.info("No documents to process. Exiting.")
        return

    # 2. Mask PII
    logger.info("Masking PII...")
    masked_documents = mask_pii_in_documents(raw_documents)

    # 3. Split Text
    logger.info("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(masked_documents)
    logger.info(f"Created {len(chunks)} chunks.")

    # 4. Initialize Embeddings
    logger.info(f"Initializing embeddings ({EMBEDDING_MODEL_NAME})...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # 5. Create/Update Vector Store
    logger.info(f"Creating/Updating Vector Store in {DB_DIR}...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    logger.info("Ingestion complete. Vector store saved.")

if __name__ == "__main__":
    ingest_data()
