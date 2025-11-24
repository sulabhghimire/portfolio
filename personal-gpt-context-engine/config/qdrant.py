import logging

from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
from qdrant_client import QdrantClient

from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

before_sleep = before_sleep_log(logger, logging.INFO)


@retry(
    wait=wait_fixed(5),  # Wait 5 seconds between each retry
    stop=stop_after_attempt(10),  # Stop after 10 attempts (50 seconds total)
    before_sleep=before_sleep,  # Log a message before sleeping
)
def connect_to_qdrant() -> QdrantClient:
    """
    Tries to connect to Qdrant with retries.
    If it fails after all retries, tenacity will re-raise the last exception.
    """
    logger.info("Attempting to connect to Qdrant...")
    if not settings:
        raise ConnectionError("Settings are not loaded, cannot connect to Qdrant.")

    return QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        api_key=settings.QDRANT_API_KEY,
    )
