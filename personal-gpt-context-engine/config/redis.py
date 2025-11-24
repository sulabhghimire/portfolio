import logging

from redis import Redis, RedisError
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log

from config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Establish a connection to the Redis server
# The decode_responses=True argument makes Redis return strings instead of bytes
before_sleep = before_sleep_log(logger, logging.INFO)


@retry(
    wait=wait_fixed(5),  # Wait 5 seconds between each retry
    stop=stop_after_attempt(10),  # Stop after 10 attempts (50 seconds total)
    before_sleep=before_sleep,  # Log a message before sleeping
)
def connect_to_redis() -> Redis:
    """
    Tries to connect to Redis with retries.
    If it fails after all retries, tenacity will re-raise the last exception.
    """
    logger.info("Attempting to connect to Redis...")
    if not settings:
        raise ConnectionError("Settings are not loaded, cannot connect to Redis.")

    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_CONTEXT_ENGINE_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )

    try:
        pong = redis_client.ping()  # Check the connection
    except RedisError as e:
        logger.exception("Redis ping failed: will retry.")

    if pong is not True and pong != "PONG":
        logger.error("Unexpected ping response from Redis: %r", pong)
        raise ConnectionError(f"Unexpected Redis ping reply: {pong!r}")

    logger.info("Connected to Redis (ping OK).")
    return redis_client
