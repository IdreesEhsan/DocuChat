from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from ..dependencies import get_current_user
from ..services.retriever import hybrid_retrieve
from ..services.llm import stream_rag_answer
import json

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/stream")
async def chat_stream(
    request: dict,  # { "query": "..." }
    current_user = Depends(get_current_user)
):
    query = request.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query' field")

    context = hybrid_retrieve(query, user_id=current_user.id, top_k=4)
    
    if not context:
        async def refusal():
            yield json.dumps({"type": "sources", "data": []}) + "\n"
            yield json.dumps({"type": "text", "data": "I cannot answer that based on your documents."}) + "\n"
        return StreamingResponse(refusal(), media_type="text/event-stream")
    
    sources_payload = []
    for chunk in context:
        sources_payload.append({
            "text": chunk['chunk_text'][:200] + "...",
            "metadata": chunk['metadata'],
            "similarity": round(chunk.get('similarity', 0), 3)
        })
    
    async def event_generator():
        yield json.dumps({"type": "sources", "data": sources_payload}) + "\n"
        async for text_chunk in stream_rag_answer(query, context):
            yield json.dumps({"type": "text", "data": text_chunk}) + "\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")