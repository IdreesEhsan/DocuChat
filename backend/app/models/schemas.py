from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChunkMetadata(BaseModel):
    source: str
    page: Optional[int] = None
    chunk_index: int
    strategy: str

class UploadResponse(BaseModel):
    status: str
    chunk_index: int
    filename: str

class ChatRequest(BaseModel):
    query: str