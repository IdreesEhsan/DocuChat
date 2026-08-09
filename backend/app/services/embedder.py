from sentence_transformers import SentenceTransformer
from core.config import settings

model = SentenceTransformer(settings.embedding_model)

def get_embedding(text: str) -> list[float]:
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def  batch_embed(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return embeddings.tolist()