import os
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────
DOCS_FOLDER  = "data/docs"
REPORT_FILE  = "data/report.txt"
CACHE_FILE   = "data/vector_store_cache.pkl"
UPLOAD_FOLDER = "data/uploads"

# ── Models ─────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")
GROQ_MODEL     = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# ── RAG ────────────────────────────────────────────
CHUNK_SIZE           = 400
CHUNK_OVERLAP        = 100
RETRIEVAL_TOP_K      = 8
RERANK_TOP_N         = 5
CONFIDENCE_THRESHOLD = 0.0001
MEMORY_MAX_TURNS     = 10

# ── Prompts ────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a helpful medical assistant with access to "
    "medical documents and patient reports."
)

REPORT_TRIGGER_WORDS = [
    "report", "patient", "my case", "my scan", "my result",
    "my diagnosis", "my condition", "my finding", "my impression",
    "my treatment", "my prognosis", "my tumor", "my mass",
    "wrong with me", "do i have", "am i"
]
