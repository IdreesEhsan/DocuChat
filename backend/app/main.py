from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import upload, chat, auth, extract   # <-- added auth, extract

app = FastAPI(title="DocuChat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)      # <-- NEW
app.include_router(extract.router)   # <-- NEW
app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"status": "DocuChat API is running"}