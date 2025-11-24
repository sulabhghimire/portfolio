import logging
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import EmbeddingType
from .embedding_model import load_embedding_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def generate_embeddings(
    texts: List[str], task_type: EmbeddingType
) -> List[List[float]]:
    """
    Generate embeddings for a text of strings using the pre-loaded local model.

    Args:
        texts (Lists[str]): A list of texts to be embedded.
        task_type: EmbeddingType enum

    Returns:
        List[List[float]]: A list of embedding vectors
    """
    logger.info(
        f"Generating embeddings for {len(texts)} texts with task_type: {task_type}..."
    )

    try:
        model = load_embedding_model()
        embeddings = model.encode(texts, show_progress_bar=False)

        logger.info("Embeddings generated successfully.")
        return embeddings.tolist()

    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}", exc_info=True)
        return []


def process_and_store_text(text: str, source_id: str) -> bool:
    """
    The main orchestrator function for the ingestion pipeline.
    It chunks text, generates embeddings, and stores them in the vector database.

    Args:
        text (str): The raw text to be processed (e.g., from a CV).
        source_id (str): A unique identifier for the document source.

    Returns:
        bool: True if successful, False otherwise.
    """
    logger.info(f"Starting ingestion pipeline for source_id: '{source_id}'")
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        text_chunks = text_splitter.split_text(text)
        logger.info(f"Text split into {len(text_chunks)} chunks.")

        if not text_chunks:
            logger.warning(
                f"No text chunks were created for source_id: '{source_id}'. Halting process."
            )
            return False

        embeddings = generate_embeddings(text_chunks, task_type="RETRIEVAL_DOCUMENT")
        if not embeddings:
            logger.error("Embedding generation failed. Halting process.")
            return False

        logger.info(f"Successfully processed and stored text for source '{source_id}'.")
        return True
    except Exception as e:
        logger.error(
            f"An error occurred during the vectorization pipeline for source '{source_id}': {e}",
            exc_info=True,
        )
        return False
