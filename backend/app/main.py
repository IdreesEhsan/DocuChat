from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import upload, chat

app = FastAPI(title="DocuChat RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credientals=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"status": "DocuChat API is running"}