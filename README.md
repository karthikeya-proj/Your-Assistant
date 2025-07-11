#  Your-Assistant: Document Q&A using LLaMA3/Mistral + FastAPI + Streamlit

Your-Assistant is a lightweight local app that allows you to upload a PDF and ask questions about its content. It uses powerful local LLMs like **LLaMA3** or **Mistral** via **Ollama**, with intelligent chunking and retrieval powered by **LlamaIndex**.

---
# Project Overview

This project consists of a FastAPI backend and a Streamlit frontend to enable PDF upload, text extraction, and querying using large language models (LLMs). The system extracts text from PDFs, indexes the content with embeddings, and answers user questions based on the document content.

---

## Features

- Upload any PDF document
- Extracts text using `pdfplumber`
- Converts and stores `.txt` versions locally
- Uses **LlamaIndex** for chunking, embedding, and indexing
- Runs LLM queries locally with **Ollama** (supports `llama3`, `mistral`, etc.)
- Clean and interactive UI via **Streamlit**

---

## Use Cases

- Legal document Q&A  
- Business report understanding    
- Research assistant for students  




## Project Structure
```
Your-Assistant/
├── main.py # FastAPI backend (upload/query)
├── streamlit_app.py # Streamlit frontend
├── requirements.txt # All Python dependencies
├── .gitignore # Ignores venv, pycache, etc.
├── data/ # Stores uploaded PDFs and extracted .txt
└── modules/
├── ollama_qa.py # Loads LLM, embeds docs, handles querying
└── doc_loader.py # Loads extracted text files for indexing

```

## requirements.txt
```
fastapi
uvicorn
streamlit
pdfplumber
requests
llama-index
llama-index-llms-ollama
llama-index-embeddings-ollama
```
------------------


| Tool / Library                    | Type         | Purpose                                                                 |
|----------------------------------|--------------|-------------------------------------------------------------------------|
| **FastAPI**                      | Backend API  | Provides upload and query endpoints (RESTful API)                      |
| **Uvicorn**                      | ASGI Server  | Runs the FastAPI app                                                   |
| **Streamlit**                    | Frontend UI  | Interactive UI for uploading PDFs and asking questions                 |
| **Ollama**                       | LLM Runtime  | Runs local LLM models like LLaMA3, Mistral                             |
| **LlamaIndex**                   | Framework    | Handles document chunking, embedding, indexing, and retrieval          |
| `llama-index-llms-ollama`        | LLM Plugin   | LLaMA3/Mistral integration via Ollama                                  |
| `llama-index-embeddings-ollama`  | Embedding    | Embedding model (e.g., `nomic-embed-text`) using Ollama                |
| **pdfplumber**                   | PDF Parser   | Extracts clean text from uploaded PDFs                                 |
| **requests**                     | HTTP Client  | Sends requests from Streamlit to FastAPI backend                       |
| **pydantic**                     | Data Model   | Validates request body in FastAPI endpoints                            |
| **os / pathlib** (Python stdlib) | Utility      | File handling and path operations                                      |
| **CORS Middleware**              | Middleware   | Allows cross-origin requests from frontend to backend                  |
| **venv / virtualenv**            | Environment  | Keeps project dependencies isolated                                    |
| **git & GitHub**                 | VCS          | Source control and code hosting                                        |

---------------
##  Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/karthikeya-proj/Your-Assistant.git
cd Your-Assistant
```

### 2. Create and Activate Virtual Environment
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt

```

### 4. Pull the Model (e.g., Mistral or LLaMA3)

```
ollama pull mistral
# or
ollama pull llama3
```

### 5. Run Backend Server
```
uvicorn main:app --reload
```

### 6. Run Streamlit App
```
streamlit run streamlit_app.py
```
##  .gitignore
```
__pycache__/
.venv/
venv/
*.pyc
*.pyo
data/*.txt
data/*.pdf
```
-------------
## How It Works

1. **Frontend** (`streamlit_app.py`) lets user upload PDF and ask a question.
2. **Backend** (`main.py`) saves PDF → extracts text → stores `.txt`.
3. LlamaIndex splits and embeds text chunks using Ollama’s `nomic-embed-text`.
4. Query goes to LLM (e.g., `llama3:8b`) locally via **Ollama**.
5. Answer is returned to Streamlit UI.
```
[User uploads PDF] → Streamlit → FastAPI (/upload)
                                ↓
                        PDF → TXT → Saved to /data

[User types question] → Streamlit → FastAPI (/query)
                                ↓
          Load .txt → Chunk → Embed → Index → Query → LLM Response
                                ↓
                        Answer returned to Streamlit UI
```


## File-by-File Explanation

### 1. `main.py` (FastAPI Backend)
- **Endpoints:**
  - `/upload/`  
    Accepts a PDF file, extracts clean text using `pdfplumber` (preferred over PyMuPDF for better text extraction), and saves the extracted content as a `.txt` file.
  - `/query/`  
    Accepts a question, model name, and file reference. Returns an answer generated by the LLM based on the indexed document content.
- **Key Features:**  
  Handles file uploads, text extraction, and query processing.

---

### 2. `streamlit_app.py` (Frontend UI)
- **User Interface:**
  - Upload PDF files.
  - Input questions related to the uploaded document.
- **Functionality:**
  - Sends requests to the FastAPI backend using `requests.post(...)`.
  - Displays the LLM-generated answers in a `st.text_area()` widget.

---

### 3. `modules/ollama_qa.py`
- **Core Module Responsibilities:**
  - Generates embeddings using Ollama embedding model: `nomic-embed-text`.
  - Initializes LLMs such as `mistral` or `llama3:8b`.
  - Processes `.txt` files by chunking, embedding, and indexing their content.
  - Handles query processing via `engine.query(question)` to return relevant answers.

---

### 4. `modules/doc_loader.py`
- **Helper Module:**
  - Loads `.txt` files as documents.
  - Prepares documents for embedding and indexing.
  - Supports modular design by separating document loading logic.

---

## `data/` Folder
- Stores uploaded PDF files (e.g., `resume.pdf`).
- Stores converted `.txt` files (e.g., `resume.txt`).
- Keeps file access local and fast for efficient processing.

---


##  Credits
* LlamaIndex

* Ollama

* Meta’s LLaMA

* Streamlit

-------
### Built with ❤️ by Karthikeya


