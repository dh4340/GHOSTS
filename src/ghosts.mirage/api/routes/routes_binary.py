from fastapi import APIRouter, Response
from io import BytesIO
from faker import Faker
import random
from utils.helper import generate_random_name
import app_logging

router = APIRouter()
fake = Faker()

logger = app_logging.setup_logger("app_logger")


@router.get("/binary", tags=["Binary"])
@router.post("/binary", tags=["Binary"])
@router.get("/binary/{file_name}", tags=["Binary"])
@router.post("/binary/{file_name}", tags=["Binary"])
def return_binary(file_name: str = None) -> Response:
    """
    Generate and return a binary file as a response.

    If `file_name` is provided, it will be used as the name of the file;
    otherwise, a random file name will be generated. The binary content
    is generated using Faker and ranges in size from 1000 to 300000 bytes.

    Args:
        file_name (str, optional): The name of the binary file. Defaults to None.

    Returns:
        Response: A FastAPI Response object containing binary data and
        a content disposition header to trigger a file download.
    """
    if file_name is None:
        file_name = generate_random_name(".bin")
        logger.info("Generated random file name: %s", file_name)

    # Generate random binary content
    binary_length = random.randint(1000, 300000)
    logger.debug("Generating binary content of length: %d bytes", binary_length)
    buf = BytesIO(fake.binary(length=binary_length))

    # Create a response with binary content and set the correct media type
    response = Response(content=buf.getvalue(), media_type="application/octet-stream")

    # Set the content disposition header for file download
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    logger.info("Serving binary file: %s", file_name)

    return response
