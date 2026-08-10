from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..core.auth import get_current_user
from ..services.llm import call_llm_with_retry
import json

router = APIRouter(prefix="/extract", tags=["Extraction"])

class ExtractRequest(BaseModel):
    text: str
    schema_description: str  # e.g., "Extract name, email, phone, skills as array"

class ExtractResponse(BaseModel):
    extracted: dict
    tokens_used: int

@router.post("/", response_model=ExtractResponse)
async def extract_structured(
    req: ExtractRequest,
    current_user: dict = Depends(get_current_user)   # <-- Protected
):
    # Load extraction prompt
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
        tokens_used = len(response.split())  # approximate
        return ExtractResponse(extracted=extracted, tokens_used=tokens_used)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="LLM returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")