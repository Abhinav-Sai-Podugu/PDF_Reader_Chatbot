# 📚 PDF Reader Chatbot

An AI-powered Streamlit web app that lets you **chat with your PDF documents** using the **Mistral-7B model via OpenRouter**. Upload one or more PDFs, ask questions in natural language, and get precise answers based **only on the content of the documents**.

---

## 🚀 Features

- 📄 Upload one or multiple PDF files
- 🤖 Ask natural questions about the uploaded content
- 🧠 Uses LangChain + Chroma for Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search with HuggingFace embeddings (`all-MiniLM-L6-v2`)
- 🔗 LLM backend via OpenRouter (Mistral-7B-Instruct or others)
- 💬 Clean chat interface powered by `streamlit-chat`

---

## 🧱 Tech Stack

| Tool             | Purpose                                |
|------------------|----------------------------------------|
| `Streamlit`      | Web interface                          |
| `LangChain`      | RAG pipeline, retrieval & chaining     |
| `Chroma`         | Local vector database                  |
| `HuggingFace`    | Embeddings for semantic search         |
| `OpenRouter`     | LLM API compatible with OpenAI SDK     |
| `PyPDF2`         | PDF text extraction                    |

---

## 🖥️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Abhinav-Sai-Podugu/PDF_Reader_Chatbot.git
cd PDF_Reader_Chatbot

### 2. Create & Activate Virtual Environment (Optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # on Linux/macOS
.venv\Scripts\activate      # on Windows

