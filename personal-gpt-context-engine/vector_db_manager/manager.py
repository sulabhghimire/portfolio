import logging
from typing import List, Optional

from qdrant_client import QdrantClient, qdrant_exceptions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class VectorDBManager:
    _client: Optional[QdrantClient]
    _collection_name: str = "personal_gpt_collection"

    def set_client(self, client: QdrantClient):
        """Injects the live, connected Qdrant client at application startup."""
        logger.info("Qdrant client has been attached to VectorDBManager.")
        self._client = client

    @property
    def client(self) -> QdrantClient:
        """Provides access to the client, ensuring it has been set."""
        if self._client is None:
            raise ConnectionError(
                "Qdrant client has not been initialized. Check application startup."
            )
        return self._client

    def ensure_collection_exists(self):
        """
        Checks if the collection exists and creates it if it doesn't.
        """
        try:
            self.client.get_collection(collection_name=self._collection_name)
            logger.info(f"Collection '{self._collection_name}' already exists.")
        except (
            qdrant_exceptions.UnexpectedResponse,
            ValueError,
        ):  # Catching potential errors if collection not found
            logger.info(
                f"Collection '{self._collection_name}' not found. Creating it now."
            )
            embedding_dim = (
                embedding_model_manager.get_model().get_sentence_embedding_dimension()
            )
            self.client.recreate_collection(
                collection_name=self._collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_dim, distance=models.Distance.COSINE
                ),
            )
            logger.info(f"Successfully created collection '{self._collection_name}'.")
