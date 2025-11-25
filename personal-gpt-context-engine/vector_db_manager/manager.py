import logging
from typing import List, Optional, Dict

from qdrant_client import QdrantClient, models

from utils import generate_unique_id
from services import load_embedding_model

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
        except Exception:  # Catching potential errors if collection not found
            logger.info(
                f"Collection '{self._collection_name}' not found. Creating it now."
            )
            embedding_dim = load_embedding_model().get_sentence_embedding_dimension()
            self.client.recreate_collection(
                collection_name=self._collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_dim, distance=models.Distance.COSINE
                ),
            )
            logger.info(f"Successfully created collection '{self._collection_name}'.")

    def _build_filter_from_metadata(
        self, metadata_filter: Dict[str, any]
    ) -> models.Filter:
        """
        A helper to dynamically build a Qdrant filter from a metadata dictionary.
        """
        return models.Filter(
            must=[
                models.FieldCondition(key=key, match=models.MatchValue(value=value))
                for key, value in metadata_filter.items()
            ]
        )

    def delete_points_by_metadata(self, metadata_filter: Dict[str, any]):
        """
        Atomically replaces all points matching a metadata filter with new points.


        Args:
            text_chunks (List[str]): List of original text pieces.
            embeddings (List[List[float]]): The corresponding vector embedding
            metadata_filter Dict[str,any]: The metadata to identify old points for deletion
        """

        logger.info(f"Deleting existing points matching filter: {metadata_filter}")
        db_filter = self._build_filter_from_metadata(metadata_filter=metadata_filter)

        self._client.delete(
            collection_name=self._collection_name,
            points_selector=models.FilterSelector(filter=db_filter),
            wait=True,
        )
        logger.info("Deletion of old points complete.")

    def upsert_points(
        self,
        text_chunks: List[str],
        embeddings: List[List[float]],
        metadata: Dict[str, any],
    ):
        """
        Builds and upserts a list of points (rows) into the Qdrant collection.
        This method only adds new data.

        Args:
            text_chunks (List[str]): The list of original text pieces.
            embeddings (List[List[float]]): The corresponding vector embeddings.
            metadata (dict): A dictionary of metadata to be associated with every chunk.
        """

        if not text_chunks:
            logger.warning("upsert_points called with no text chunks. Nothing to do.")
            return

        points_to_insert = []
        for i, chunk in enumerate(text_chunks):
            point_id = str(generate_unique_id())

            point_metadata = metadata.copy()
            point_metadata["chunk_index"] = i

            payload = {"text_chunk": chunk, "metadata": point_metadata}

            points_to_insert.append(
                models.PointStruct(id=point_id, vector=embeddings[i], payload=payload)
            )

        logger.info(
            f"Preparing to upsert {len(points_to_insert)} points with base metadata: {metadata}"
        )

        self.client.upsert(
            collection_name=self._collection_name, points=points_to_insert, wait=True
        )
        logger.info(f"Successfully upserted {len(points_to_insert)} points.")


vector_db_manager = VectorDBManager()
