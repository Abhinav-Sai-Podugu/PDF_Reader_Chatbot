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
