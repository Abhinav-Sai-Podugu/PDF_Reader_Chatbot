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
```

### 2. Create & Activate Virtual Environment (Optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # on Linux/macOS
.venv\Scripts\activate      # on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Key Setup

### 1. Create a .env file in the project root:

```bash
touch .env  # or manually create it
```

### 2. Paste your OpenRouter API credentials:

```bash
OPENAI_API_KEY=your-openrouter-api-key
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

### 3. Don't have a key? Get one at:

👉 https://openrouter.ai

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then visit http://localhost:8501 in your browser.

---

## 📁 File Structure

```bash
PDF_Reader_Chatbot/
│
├── app.py              # Main Streamlit app
├── .env.template       # Example env file (NO real keys)
├── .gitignore          # Excludes .env, .venv, etc.
├── requirements.txt    # All dependencies
├── README.md           # You’re here!
└── chroma_data/        # Persistent vector DB (created at runtime)
```

---

## 🧪 How It Works

1. PDF Upload → PyPDF2 extracts text

2. Text Chunking → Split into overlapping chunks with LangChain

3. Embeddings → Created using all-MiniLM-L6-v2 model from HuggingFace

4. Vector DB → Stored in Chroma for fast semantic retrieval

5. Multi-Query Retriever → Improves document match quality

6. LLM Chain → LLM answers based on retrieved context only

   
