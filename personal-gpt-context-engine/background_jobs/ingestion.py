import logging

from job_manager import job_manager
from resume_parser import extract_text_from_pdf

from models import JobStatus, JobStage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def run_cv_ingestion_job(job_id: str, file_bytes: bytes, filename: str):
    """Background job to ingest and process the uploaded CV."""
    logger.info(f"Starting CV ingestion job_id: {job_id}, filename: {filename}.")

    try:
        # Perform Text Extraction
        job_manager.update_job(
            job_id=job_id,
            updates={
                "job_stage": JobStage.EXTRACTING_TEXT,
                "status": JobStatus.RUNNING,
                "details": "Extracting text from the uploaded CV.",
            },
        )

        extracted_text = await extract_text_from_pdf(file_bytes)
        logger.info(f"CV ingestion job_id: {job_id}, filename: {filename} completed.")

        if not extracted_text:
            logger.info(
                f"CV ingestion job_id: {job_id}, filename: {filename}. No text extracted."
            )
            job_manager.update_job(
                job_id=job_id,
                updates={
                    "status": JobStatus.FAILED,
                    "errorMsg": "Critical error: Failed to extract text from PDF.",
                },
            )
            return

        # TODO: The perform vectorization step would go here

        job_manager.update_job(
            job_id=job_id,
            updates={
                "status": JobStatus.COMPLETED,
                "stage": JobStatus.COMPLETED,
                "details": "CV has been successfully parsed.",
            },
        )
        logger.info(f"Successfully completed job {job_id}")

    except Exception as e:
        logger.error(
            f"An unexpected error occurred during cv ingestion for job {job_id}: {e}",
            exc_info=True,
        )
        job_manager.update_job(
            job_id=job_id,
            updates={
                "status": JobStatus.FAILED,
                "errorMsg": f"An unexpected error occurred: {str(e)}",
            },
        )
