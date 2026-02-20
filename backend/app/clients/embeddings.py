"""
HuggingFace embeddings client (optional feature).
Only loaded if ENABLE_HF_EMBEDDINGS=true
"""
from typing import Optional, List
from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingsClient:
    """Client for generating text embeddings using HuggingFace models."""
    
    def __init__(self):
        self.enabled = settings.ENABLE_HF_EMBEDDINGS
        self.model = None
        
        if self.enabled:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(settings.HF_MODEL_NAME)
                logger.info(f"HF embeddings enabled: {settings.HF_MODEL_NAME}")
            except ImportError:
                logger.warning("sentence-transformers not installed, embeddings disabled")
                self.enabled = False
            except Exception as e:
                logger.error(f"Failed to load embeddings model: {e}")
                self.enabled = False
    
    def is_available(self) -> bool:
        """Check if embeddings are available."""
        return self.enabled and self.model is not None
    
    def encode(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for text.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            List of embedding vectors, or None if not available
        """
        if not self.is_available():
            return None
        
        try:
            embeddings = self.model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Embeddings generation failed: {e}")
            return None
    
    def encode_single(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string to encode
            
        Returns:
            Embedding vector, or None if not available
        """
        result = self.encode([text])
        if result:
            return result[0]
        return None


# Singleton instance
embeddings_client = EmbeddingsClient()
