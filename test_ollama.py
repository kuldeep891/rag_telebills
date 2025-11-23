from langchain_ollama import OllamaLLM
import sys

def test_ollama_connection():
    model_name = "phi3" # Ensure this matches what you pulled
    print(f"Testing connection to Ollama (model: {model_name})...")
    
    try:
        llm = OllamaLLM(model=model_name)
        response = llm.invoke("Say 'Hello, World!' if you can hear me.")
        print("\nSuccess! Response from Ollama:")
        print("-" * 20)
        print(response)
        print("-" * 20)
    except Exception as e:
        print("\nError connecting to Ollama:")
        print(e)
        print("\nTroubleshooting Tips:")
        print("1. Ensure Ollama is running (check system tray).")
        print(f"2. Ensure you have pulled the model: 'ollama pull {model_name}'")

if __name__ == "__main__":
    test_ollama_connection()
