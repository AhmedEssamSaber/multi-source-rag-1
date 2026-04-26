# 🧠 Medical RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for medical documents and patient reports.  
Built with Cohere Embeddings, Cohere Reranker, and Groq LLM.

---

## 📁 Project Structure

```
project/
│
├── main.py                  # FastAPI entry point
├── chatbot.py               # Main chatbot logic (also CLI)
├── requirements.txt
├── .env                     # Your API keys (never commit)
├── .env.example             # Keys template
├── .gitignore
│
├── config/
│   └── settings.py          # All constants and config in one place
│
├── app/
│   ├── core/
│   │   ├── chunker.py       # Text chunking
│   │   ├── embedder.py      # Cohere embeddings + reranker
│   │   ├── vector_store.py  # In-memory store + cache
│   │   ├── memory.py        # Conversation memory
│   │   ├── prompt_builder.py# Prompt construction
│   │   └── generator.py     # Groq LLM
│   │
│   ├── api/
│   │   └── routes.py        # API endpoints
│   │
│   └── models/
│       └── schemas.py       # Request/Response schemas
│
└── data/
    ├── report.txt           # Patient report
    ├── vector_store_cache.pkl (auto-generated)
    ├── uploads/             # Future: uploaded reports
    └── docs/
        ├── brain_edema.txt
        ├── brain_tumors.txt
        ├── glioma.txt
        ├── hydrocephalus.txt
        ├── mass_effect.txt
        ├── meningioma.txt
        └── pituitary_adenoma.txt
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys in .env
```

---

## 🚀 Running

**API:**
```bash
uvicorn main:app --reload
```

**CLI:**
```bash
python chatbot.py
```

---

## 📡 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Health check |
| GET    | `/health`| Chunks + memory status |
| POST   | `/chat`  | Send query, get answer |
| POST   | `/reset` | Clear conversation memory |

**Swagger UI:** `http://localhost:8000/docs`

---

## 🔗 Frontend Example

```javascript
const res = await fetch("http://localhost:8000/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "explain my patient report" })
});
const data = await res.json();
// data.answer | data.sources | data.confidence_label
```
