from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..models.schemas import ChatRequest
from ..services.retriever import hybrid_retrieve
from ..services.llm import stream_rag_answer
import json

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    try:
        context = hybrid_retrieve(request.query, top_k=4)

        if not context:
            async def refusal():
                yield json.dumps({"type": "sources", "data": []}) + "\n"
                yield json.dumps({"type": "text", "data": "I cannot answer that based on the provided documents."}) + "\n"
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
            async for text_chunk in stream_rag_answer(request.query, context):
                yield json.dumps({"type": "text", "data": text_chunk}) + "\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    