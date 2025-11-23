# Setting up Ollama on Windows

Ollama is a tool that allows you to run open-source large language models (LLMs) locally on your machine.

## 1. Download and Install
1. Visit the official download page: [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. Click **"Download for Windows"**.
3. Run the downloaded installer (`OllamaSetup.exe`).
4. Follow the installation prompts.

## 2. Verify Installation
Open a **new** PowerShell or Command Prompt window (to ensure the path is updated) and run:
```powershell
ollama --version
```
You should see the installed version number.

## 3. Pull the Model
For this project, we are using **Phi-3** (a lightweight but powerful model) or **Llama 3**. Run one of the following commands in your terminal:

**Option A: Phi-3 (Recommended for lower resources)**
```powershell
ollama pull phi3
```

**Option B: Llama 3 (Better performance if you have 8GB+ RAM)**
```powershell
ollama pull llama3
```

## 4. Test the Model
Once pulled, you can test it immediately:
```powershell
ollama run phi3 "Tell me a joke about Python programming."
```
If it responds, you are ready to go!

## 5. Keep Ollama Running
Ollama usually runs in the background (you'll see an icon in the system tray). If it's not running, you can start it by searching for "Ollama" in the Start menu. The Python script `src/query.py` will communicate with this background service.
