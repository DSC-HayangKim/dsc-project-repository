from sentence_transformers import SentenceTransformer

# Singleton instance
_model = None

def get_model():
    global _model
    if _model is None:
        # Force CPU as requested
        device = "cpu"
        print(f"Loading embedding model on {device}...")
        _model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS", device=device)
    return _model

def get_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for the given text using KR-SBERT.
    """
    model = get_model()
    # Encode returns a numpy array, convert to list
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()
