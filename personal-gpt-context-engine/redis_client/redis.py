from redis import Redis, exceptions as redis_exceptions
import json
import logging
from typing import Optional
from datetime import datetime, timezone

from models import JobStatus, ProcessingJobType, JobStage, ProcessingJob
from config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Establish a connection to the Redis server
# The decode_responses=True argument makes Redis return strings instead of bytes
try:
    print(settings)
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_CONTEXT_ENGINE_DB,
        username=settings.REDIS_USER_NAME,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        health_check_interval=200,
    )
    redis_client.ping()  # Check the connection
    logger.info("Successfully connected to Redis.")
except redis_exceptions.ConnectionError as e:
    logger.error(f"Failed to connect to Redis server: {e}")
    redis_client = None


class JobStatusManager:
    """
    Manages storing and retrieving job status information in Redis.
    """

    def __init__(self, client: Redis):
        if not client:
            raise ConnectionError("Redis client is not initialized.")
        self.client = redis_client
        self.key_prefix = "processing_job"

    def _get_key(self, job_id: str) -> str:
        """Generate Redis key for a given job ID."""
        return f"{self.key_prefix}:{job_id}"

    def get_job(self, job_id: str) -> Optional[ProcessingJob]:
        """Retrieve job status from Redis."""
        job_key = self._get_key(job_id)
        job_data = self.client.get(job_key)
        if job_data:
            try:
                job_dict = json.loads(job_data)
                return ProcessingJob(**job_dict)
            except json.JSONDecodeError as e:
                logger.error(
                    f"Error decoding job data from Redis for job_id {job_id}: {e}"
                )
                return None

        return None

    def create_job(
        self, job_id: str, job_type: ProcessingJobType, filename: Optional[str] = None
    ) -> ProcessingJob:
        """Creates a new job with an initial 'PENDING'/'QUEUED' state."""

        initial_job = ProcessingJob(
            job_id=job_id,
            job_type=job_type,
            job_stage=JobStage.QUEUED,
            status=JobStatus.PENDING,
            details=f"Job '{job_id}' has been created and is waiting to be processed.",
            filename=filename,
        )

        job_key = self._get_key(job_id)
        self.client.set(job_key, initial_job.json())
        logger.info(f"Created new job '{job_id}' of type '{job_type.value}'.")
        return initial_job

    def update_job(self, job_id: str, updates: dict) -> Optional[ProcessingJob]:
        """Update job status in Redis."""
        job = self.get_job(job_id)
        if not job:
            logger.warning(f"Job with ID {job_id} not found in Redis for update.")
            return None

        job_dict = job.model_dump()
        job_dict.update(updates)

        job_dict["updated_at"] = datetime.now(timezone.utc)

        try:
            updated_job = ProcessingJob(**job_dict)

            job_key = self._get_key(job_id)
            self.client.set(job_key, updated_job.json())
            logger.info(
                f"Updated job '{job_id}'. New status: {updated_job.status.value}, Stage: {updated_job.job_stage.value}"
            )
            return updated_job
        except Exception as e:
            logger.error(f"Failed to update job '{job_id}' due to invalid data: {e}")
            return None


job_manager = JobStatusManager(redis_client) if redis_client else None
