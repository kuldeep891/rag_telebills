import os
import argparse
import logging
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "phi3" 

def query_rag(query_text: str, prompt_template: str = None):
    # 1. Initialize Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # 2. Load Vector Store
    if not os.path.exists(DB_DIR):
        logger.error(f"Vector store not found at {DB_DIR}. Please run ingest.py first.")
        return

    vector_store = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

    # 3. Initialize LLM
    try:
        llm = OllamaLLM(model=LLM_MODEL)
    except Exception as e:
        logger.error(f"Failed to initialize Ollama: {e}")
        return

    # 4. Define Prompt
    if not prompt_template:
        prompt_template = """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 5. Create Chains
    # Create a chain that takes documents and a question and returns an answer
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create the retrieval chain that retrieves docs and then passes them to the document chain
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # 6. Execute Query
    logger.info(f"Querying: {query_text}")
    
    # Note: create_retrieval_chain expects 'input' key for the question
    response = retrieval_chain.invoke({"input": query_text})
    
    print("\n=== Answer ===")
    print(response['answer'])
    
    print("\n=== Sources ===")
    if 'context' in response:
        for doc in response['context']:
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', '?')
            print(f"- {os.path.basename(source)} (Page {page})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the RAG pipeline.")
    parser.add_argument("query", type=str, help="The question to ask.")
    parser.add_argument("--prompt", type=str, help="Custom prompt template. Must include {context} and {input}.", default=None)
    args = parser.parse_args()
    
    query_rag(args.query, args.prompt)
