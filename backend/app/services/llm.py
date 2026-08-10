import tiktoken
import asyncio
import uuid
from groq import Groq, APIError, RateLimitError
from ..core.config import settings
from ..utils.logger import log_cost

client = Groq(api_key=settings.groq_api_key)
enc = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

def build_messages(query: str, context_chunks: list[dict]):
    context_text = ""
    for i, chunk in enumerate(context_chunks):
        src = chunk['metadata'].get('source', 'unknown')
        page = chunk['metadata'].get('page', 'N/A')
        context_text += f"\n[Document {i+1}] Source: {src} (Page {page})\n{chunk['chunk_text']}\n"
    
    with open("prompts/rag_system.txt", "r") as f:
        system_prompt = f.read()
    system_prompt = system_prompt.replace("{{CONTEXT}}", context_text)
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {query}"}
    ]

async def stream_rag_answer(query: str, context_chunks: list[dict]):
    request_id = str(uuid.uuid4())[:8]
    messages = build_messages(query, context_chunks)
    
    prompt_text = " ".join([m["content"] for m in messages])
    prompt_tokens = count_tokens(prompt_text)
    
    retries = 0
    while retries < 3:
        try:
            stream = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                temperature=0.2,
                max_tokens=1024,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            completion_tokens = count_tokens(full_response)
            cost = (prompt_tokens + completion_tokens) * 0.00000059
            log_cost(request_id, settings.llm_model, prompt_tokens, completion_tokens, cost)
            break
            
        except (RateLimitError, APIError) as e:
            retries += 1
            if retries >= 3:
                yield f"⚠️ Error after 3 retries: {str(e)}"
                break
            await asyncio.sleep(2 ** retries)
            yield f"🔄 Retrying... ({retries}/3)\n"

# NEW: Non-streaming call for extraction (Week 2)
async def call_llm_with_retry(messages, temperature=0.2, max_tokens=1024):
    retries = 0
    while retries < 3:
        try:
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except (RateLimitError, APIError) as e:
            retries += 1
            if retries >= 3:
                raise e
            await asyncio.sleep(2 ** retries)