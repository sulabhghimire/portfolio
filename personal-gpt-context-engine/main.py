import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks

from config import settings
from background_jobs import run_cv_ingestion_job
from models import ProcessingJobType, ProcessingJobResponse
from utils import generate_unique_id

from config import connect_to_redis
from job_manager import job_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = connect_to_redis()
    job_manager.set_client(redis)
    yield


app = FastAPI(title="Personal GPT Context Engine", version="1.0.0", lifespan=lifespan)


@app.post(
    "/api/v1/upload",
    summary="Upload a CV for processing",
    response_model=ProcessingJobResponse,
    status_code=202,
)
async def upload_cv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Upload your CV in PDF format"),
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a PDF file."
        )

    file_bytes = await file.read()

    # Create a unique job ID
    job_id = generate_unique_id(prefix="cv")

    # Create a new job in Redis
    job = job_manager.create_job(
        job_id=job_id, job_type=ProcessingJobType.CV_INGESTION, filename=file.filename
    )

    # Add cv ingestion job to background
    background_tasks.add_task(
        run_cv_ingestion_job,
        job_id=job_id,
        file_bytes=file_bytes,
        filename=file.filename,
    )

    # prepare a response
    response = ProcessingJobResponse(
        message="CV upload successful. Processing has started.",
        success=True,
        data=job,
    )

    return response


@app.get("/api/v1/jobs", summary="Fetch all job summary status")
async def subscribe_to_job_status():
    return


def main():

    if not settings:
        print("FATAL: Couldn't load settings. Exiting.")
        return

    print("Starting Personal GPT Context Engine")
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
