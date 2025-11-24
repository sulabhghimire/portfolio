import logging
from typing import Optional

from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

MODEL_NAME = "BAAI/bge-small-en-v1.5"

_embedding_model: Optional[SentenceTransformer] = None


def load_embedding_model():
    """
    Loads the Sentence Transformer model into memory.
    This function is called once during application startup.
    """
    global _embedding_model

    if _embedding_model is None:
        logger.info(
            f"Model is not loaded. Initializing '{MODEL_NAME}' in current process..."
        )
        try:
            # This line will run once per worker process.
            _embedding_model = SentenceTransformer(MODEL_NAME)
            logger.info(f"Model '{MODEL_NAME}' loaded successfully.")
        except Exception as e:
            logger.critical(
                f"FATAL: Failed to load the embedding model '{MODEL_NAME}'. Error: {e}",
                exc_info=True,
            )
            # Raising an exception here will cause the request to fail,
            # which is the correct behavior.
            raise

    return _embedding_model
