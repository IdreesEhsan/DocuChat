from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, upload, chat, extract

app = FastAPI(title="DocuChat RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(extract.router)

@app.get("/")
async def root():
    return {"status": "DocuChat API is running"}