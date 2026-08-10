from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..core.auth import get_current_user
from ..services.parser import parse_file
from ..services.chunker import chunk_document
from ..services.embedder import batch_embed
from ..core.supabase import supabase
from ..models.schemas import UploadResponse
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)   # <-- Protected
):
    try:
        raw_text, meta = await parse_file(file)
        chunks = chunk_document(raw_text, meta["source"], strategy="recursive")
        
        texts = [c["text"] for c in chunks]
        embeddings = batch_embed(texts)
        
        rows = []
        for chunk, emb in zip(chunks, embeddings):
            rows.append({
                "id": str(uuid.uuid4()),
                "user_id": current_user["id"],     # <-- Scope to user
                "chunk_text": chunk["text"],
                "metadata": chunk["metadata"],
                "embedding": emb
            })
        
        supabase.table("documents").insert(rows).execute()
        
        return UploadResponse(status="success", chunks_stored=len(rows), filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))