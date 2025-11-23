# RAG Pipeline for Telephone Bills

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline to query telephone bill PDFs. It features **PII (Personally Identifiable Information) masking** to protect sensitive user data before storing it in a vector database.

## Features
- **PDF Ingestion**: Loads telephone bill PDFs from a data directory.
- **PII Masking**: Uses **Microsoft Presidio** to detect and mask sensitive entities (Names, Phone Numbers, Emails, SSNs) *before* embedding.
- **Vector Storage**: Stores text embeddings locally using **ChromaDB** and **HuggingFace Embeddings** (`all-MiniLM-L6-v2`).
- **Local LLM**: Uses **Ollama** (Phi-3 or Llama 3) for private, offline query generation.
- **Customizable Retrieval**: Uses LangChain's modern chain architecture for flexible querying.

## Prerequisites
- **Python 3.11** (Recommended)
- **Ollama**: Installed and running ([Download](https://ollama.com/download)).
- **Git**

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/kuldeep891/rag_telebills.git
    cd rag_telebills
    ```

2.  **Create and Activate Virtual Environment**:
    ```powershell
    # Windows
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Spacy Model** (Required for PII detection):
    ```bash
    python -m spacy download en_core_web_lg
    ```

5.  **Pull Ollama Model**:
    ```bash
    ollama pull phi3
    ```

## Usage

### 1. Generate Test Data
Create sample telephone bills with randomized PII:
```bash
python create_dummy_data.py
```
*Creates 5 PDF files in the `data/` directory.*

### 2. Ingest Data
Process the PDFs, mask PII, and store vectors in ChromaDB:
```bash
python -m src.ingest
```

### 3. Query the Data
Ask questions about the bills:
```bash
python -m src.query "Who has the highest bill?"
```

**Custom Prompts:**
You can also provide a custom prompt template:
```bash
python -m src.query "Summarize the bill." --prompt "Summarize the following context: {context} Question: {input}"
```

## Project Structure
- `src/ingest.py`: Main ingestion script (Load -> Mask -> Chunk -> Embed -> Store).
- `src/query.py`: Retrieval and generation script.
- `src/utils.py`: Helper class for PII masking using Presidio.
- `create_dummy_data.py`: Script to generate synthetic PDF bills.
- `inspect_db.py`: Utility to inspect the contents of the vector database.
