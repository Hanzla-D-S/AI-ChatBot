---
title: Shopeasy Chatbot
emoji: 🛒
colorFrom: blue
colorTo: blue
sdk: docker
pinned: false
---

# ShopEasy AI Customer Support Chatbot

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-brightgreen)

An AI-powered customer support chatbot built with RAG, LangChain, FastAPI and Streamlit.

🔗 **[Live Demo](https://hanzlainam-shopeasy-chatbot.hf.space)**

---

## Features
- RAG-powered answers from company documents
- Conversational memory
- FastAPI backend
- Streamlit chat UI
- Dockerized
- CI/CD with GitHub Actions

---

## Tech Stack
| Layer | Technology |
|---|---|
| LLM | OpenAI GPT-3.5-turbo |
| RAG | LangChain + FAISS |
| Backend | FastAPI |
| Frontend | Streamlit |
| DevOps | Docker + GitHub Actions |
| Deployment | Hugging Face Spaces |

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-support-chatbot.git
cd ai-support-chatbot
```

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Set up environment
```bash
echo "OPENAI_API_KEY=your_key" > .env
```

### 4. Build vector store
```bash
python backend/ingest.py
```

### 5. Run
```bash
# Terminal 1
uvicorn backend.main:app --reload

# Terminal 2
streamlit run frontend/app.py
```

---

## Author
**Muhammad Hanzla**
- hanzlainam204@gmail.com
- [LinkedIn](https://www.linkedin.com/in/muhammad-hanzla-data-science/)
- [GitHub](https://github.com/Hanzla-D-S?tab=repositories)