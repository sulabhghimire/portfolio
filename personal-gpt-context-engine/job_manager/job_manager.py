import json
import logging

from redis import Redis
from typing import Optional
from datetime import datetime, timezone

from models import JobStatus, ProcessingJobType, JobStage, ProcessingJob


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class _JobStatusManager:
    """Manages storing and retrieving job status information in Redis."""

    _client: Redis = None  # The client will be attached at startup
    key_prefix = "processing_job"

    def set_client(self, client: Redis):
        """Attaches the active Redis client to the manager instance."""
        logger.info("Redis client has been attached to JobStatusManager.")
        self._client = client

    @property
    def client(self) -> Redis:
        """Provides access to the client, ensuring it has been set."""
        if self._client is None:
            raise ConnectionError(
                "Redis client has not been initialized. The app may be starting up or the connection failed."
            )
        return self._client

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


job_manager = _JobStatusManager()
