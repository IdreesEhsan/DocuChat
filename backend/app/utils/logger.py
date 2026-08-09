import json
import os
from datetime import datetime

LOG_DIR = 'logs'
os.makedirs(LOG_DIR,exist_ok=True)

def log_cost(request_id: str, model: str, prompt_tokens: int, completion_tokens: int, cost_usd: float):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "cost_usd": round(cost_usd, 6)
    }
    with open(f"{LOG_DIR}/cost_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"💰 Cost Log: {entry}")