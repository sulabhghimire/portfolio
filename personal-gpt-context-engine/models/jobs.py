from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone

from typing import Optional


class EmbeddingType(str, Enum):
    """
    Enumeration of task type for embedding model.
    """

    RETRIEVAL_DOCUMENT = "retrieval document"
    RETRIEVAL_QUERY = "retrieval query"


class JobStatus(str, Enum):
    """
    Enumeration of possible job statuses.
    """

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobStage(str, Enum):
    """
    Specific stage of the CV ingestion process.
    """

    QUEUED = "QUEUED"
    EXTRACTING_TEXT = "EXTRACTING_TEXT"
    VECTORIZATION = "VECTORIZATION"
    COMPLETED = "COMPLETED"


class ProcessingJobType(str, Enum):
    """
    Type of processing job.
    """

    CV_INGESTION = "CV_INGESTION"
    GITHUB_REPO_INGESTION = "GITHUB_REPO_INGESTION"
    LINKEDIN_PROFILE_INGESTION = "LINKEDIN_PROFILE_INGESTION"


class ProcessingJob(BaseModel):
    """
    Model representing a resume processing job.
    """

    job_id: str = Field(..., description="Unique identifier for the job")
    job_type: ProcessingJobType = Field(..., description="Type of the processing job")
    job_stage: JobStage = Field(..., description="Type of the processing job stage")
    status: JobStatus = Field(..., description="Current status of the job")
    details: str = Field(..., description="Details about the job")
    errorMsg: Optional[str] = Field(None, description="Error message if the job failed")
    filename: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the job was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the job was last updated",
    )


class ProcessingJobResponse(BaseModel):
    """
    Response model for processing job status.
    """

    data: ProcessingJob = Field(..., description="Processing job details")
    message: str = Field(..., description="Response message")
    success: bool = Field(..., description="Indicates if the request was successful")
