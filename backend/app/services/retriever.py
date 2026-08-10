from ..services.db_service import supabase
from .embedder import get_embedding

def hybrid_retrieve(query: str, user_id: str, top_k: int = 5):
    query_emb = get_embedding(query)
    
    # Vector search via RPC (returns all, we filter by user_id)
    vector_results = supabase.rpc(
        "match_documents",
        {"query_embedding": query_emb, "match_threshold": 0.72, "match_count": top_k}
    ).execute()
    
    # Filter by user_id
    user_results = [r for r in vector_results.data if r.get("user_id") == user_id]
    if user_results:
        return user_results
    
    # Fallback keyword search with user filter
    text_results = supabase.table("documents") \
        .select("*") \
        .eq("user_id", user_id) \
        .ilike("chunk_text", f"%{query}%") \
        .limit(top_k) \
        .execute()
    
    return text_results.data if text_results.data else []