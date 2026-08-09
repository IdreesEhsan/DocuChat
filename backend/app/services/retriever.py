from ..core.supabase import supabase
from .embedder import get_embedding

def hybrid_retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_emb = get_embedding(query)

    vector_results = supabase.rpc(
        "match_documents",
        {"query_embedding": query_emb, "match_threshold": 0.72, "match_count": top_k}
    ).execute()

    if vector_results.data and len(vector_results.data) > 0:
        return vector_results.data

    text_results = supabase.table("documents") \
        .select("*") \
        .ilike("chunk_text", f"%{query}%") \
        .limit(top_k) \
        .execute()

    return text_results.data if text_results.data else []