import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union


class EmbeddingEngine:
    _instance = None
    _model = None

    def __new__(cls):
        # Singleton pattern to prevent loading the model multiple times in memory
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)
            # Efficient, lightweight, high-performance general embedding model
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._instance

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Converts a text string or list of text strings into 384-d float32 vectors.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # normalize_embeddings=True allows calculating cosine similarity via dot product
        embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return embeddings