from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..dependencies import get_current_user
from ..services.llm import call_llm_with_retry
import json

router = APIRouter(prefix="/extract", tags=["extract"])

class ExtractRequest(BaseModel):
    text: str
    schema_description: str

@router.post("/")
async def extract_structured(
    req: ExtractRequest,
    current_user = Depends(get_current_user)
):
    with open("prompts/extract_system.txt", "r") as f:
        system_prompt = f.read()
    system_prompt = system_prompt.replace("{{SCHEMA}}", req.schema_description)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Extract from:\n{req.text}"}
    ]
    
    try:
        response = await call_llm_with_retry(messages, temperature=0.1, max_tokens=500)
        extracted = json.loads(response)
        return {"extracted": extracted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")