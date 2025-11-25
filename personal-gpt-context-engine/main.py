import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from starlette.concurrency import run_in_threadpool

from config import settings, connect_to_redis, connect_to_qdrant
from models import ProcessingJobType, ProcessingJobResponse
from background_jobs import run_cv_ingestion_job
from vector_db_manager import vector_db_manager
from utils import generate_unique_id

from job_manager import job_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info("Startup: connecting to Redis...")
        redis = await run_in_threadpool(connect_to_redis)
    except Exception as exc:
        logger.exception("Startup: failed to connect to Redis. Aborting startup.")
        raise

    try:
        job_manager.set_client(redis)
    except Exception:
        logger.exception(
            "Failed to set redis client on job_manager. Closing redis and aborting."
        )
        try:
            redis.close()
        except Exception:
            logger.exception(
                "Error while closing redis after failed job_manager.set_client()"
            )
        raise

    try:
        logger.info("Startup: validating Qdrant connectivity...")
        # run the blocking connect function in a threadpool and wait for it
        vector_db_client = await run_in_threadpool(connect_to_qdrant)
    except Exception:
        logger.exception(
            "Startup: failed to validate Qdrant. Cleaning up and aborting startup."
        )
        # Cleanup Redis before re-raising so we don't leak resources
        try:
            redis.close()
        except Exception:
            logger.exception(
                "Error while closing redis during shutdown after qdrant failure"
            )
        raise

    try:
        vector_db_manager.set_client(vector_db_client)
        vector_db_manager.ensure_collection_exists()
    except Exception:
        logger.exception("Failed to qdrant client to vector db.")

    logger.info("Startup: Redis connected and Qdrant reachable. Starting app.")

    try:
        yield
    finally:
        # --- Shutdown cleanup ---
        logger.info("Shutdown: closing redis client.")
        try:
            redis.close()
        except Exception:
            logger.exception("Error while closing redis on shutdown")


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
