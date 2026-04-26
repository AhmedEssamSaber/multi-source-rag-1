import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router, set_chatbot
from chatbot import Chatbot

app = FastAPI(
    title="Medical RAG Chatbot API",
    description="API for medical chatbot with multi-source retrieval",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load chatbot once and inject into routes
bot = Chatbot()
set_chatbot(bot)

app.include_router(router)
