import asyncio
import fitz
import logging

from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def _parse_pdf_sync(pdf_bytes: bytes) -> str:
    """
    Synchronously parse PDF bytes to extract text.
    Designed to be run in a separate thread to avoid blocking the event loop.
    Arguments:
        pdf_bytes (bytes): The PDF file content in bytes.
    Returns:
        str: Extracted text from the PDF.
    """
    text_content = []
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        logger.info(f"Opened PDF document with {pdf_document.page_count} pages.")

        for page in pdf_document:
            text_content.append(page.get_text())

        logger.info("Completed text extraction from PDF.")
        return "".join(text_content)
    except Exception as e:
        logger.error(f"Error while parsing PDF: {e}", exc_info=True)

        raise
    finally:
        if "pdf_document" in locals() and pdf_document:
            pdf_document.close()


async def extract_text_from_pdf(pdf_bytes: bytes) -> Optional[str]:
    """
    Asynchronous public interface for the PDF parsing pipeline.
    It runs the synchronous parsing function in a non-blocking thread.
    """
    logger.info("Starting asynchronous PDF text extraction pipeline.")

    try:
        loop = asyncio.get_running_loop()
        extracted_text = await loop.run_in_executor(
            None, _parse_pdf_sync, pdf_bytes  # Use the default ThreadPoolExecutor
        )
        return extracted_text
    except Exception as e:
        logger.error(f"Pipeline failed during execution: {e}")

        return None
