import re

def chunk_by_fixed(text: str, source: str, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append({
            "text": text[start:end],
            "metadata": {"source": source, "chunk_index": idx, "strategy": "fixed", "page": 1}
        })
        start += chunk_size - overlap
        idx += 1
    return chunks

def chunk_recursive(text: str, source: str, max_len=512):
    separators = ["\n\n", "\n", ". ", ", ", " "]
    chunks = []
    idx = 0

    def _split_recursive(t, depth=0):
        nonlocal idx
        if depth >= len(separators):
            clean = t.strip()
            if clean:
                chunks.append({"text": clean, "metadata": {"source": source, "chunk_index": idx, "strategy": "recursive", "page": 1}})
                idx += 1
            return
        parts = t.split(separators[depth])
        current = ""
        for p in parts:
            if len(current) + len(p) < max_len:
                current += p + separators if p else ""
            else:
                if current:
                    chunks.append({"text": current.strip(), "metadata": {"source": source, "chunk_index": idx, "strategy": "recursive", "page": 1}})
                    idx += 1
                    current = ""
                if len(p) > max_len:
                    _split_recursive(p, depth+1)
                else:
                    current = p + separators[depth] if p else ""
        if current:
            chunks.append({"text": current.strip(), "metadata": {"source": source, "chunk_index": idx, "strategy": "recursive", "page": 1}})
            idx += 1

    _split_recursive(text)
    return chunks

def chunk_semantic(text: str, source: str, max_tokens=512):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    idx = 0
    current = ""
    for sent in sentences:
        if len(current) + len(sent) < max_tokens * 4:
            current += sent + " "
        else:
            if current:
                chunks.append({"text": current.strip(), "metadata": {"source": source, "chunk_index": idx, "strategy": "semantic", "page": 1}})
                idx += 1
            current = sent + " "
    if current:
        chunks.append({"text": current.strip(), "metadata": {"source": source, "chunk_index": idx, "strategy": "semantic", "page": 1}})
    return chunks

def chunk_document(text: str, source: str, strategy: str = "recursive"):
    if strategy == "fixed":
        return chunk_by_fixed(text, source)
    elif strategy == "recursive":
        return chunk_recursive(text, source)
    elif strategy == "semantic":
        return chunk_semantic(text, source)
    raise ValueError("Strategy must be fixed, recursive, or semantic")