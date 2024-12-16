from io import BytesIO

from app_logging import setup_logger
from faker import Faker
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.helper import generate_random_name

router = APIRouter()
fake = Faker()

logger = setup_logger(__name__)


@router.get("/msi", tags=["Files"])
@router.post("/msi", tags=["Files"])
@router.get("/msi/{path:path}", tags=["Files"])
@router.post("/msi/{path:path}", tags=["Files"])
def return_msi(path: str = None) -> StreamingResponse:
    """Return a MSI file containing random data."""

    if path is None:
        path = generate_random_name(".msi")
    elif not path.endswith(".msi"):
        path += ".msi"  # Add .msi extension if not present

    logger.info(f"Generating MSI file: {path}")

    # Create a simple MSI file structure in memory
    msi_content = (
        f"This is a random MSI file with random content: {fake.paragraph()}".encode(
            "utf-8"
        )
    )

    # Create a BytesIO buffer to hold the MSI file
    msi_buffer = BytesIO(msi_content)

    # Seek to the beginning of the BytesIO buffer
    msi_buffer.seek(0)

    # Create the StreamingResponse
    response = StreamingResponse(
        msi_buffer,
        media_type="application/x-msdownload",
        headers={"Content-Disposition": f"attachment; filename={path}"},
    )

    logger.info("MSI file generated successfully.")

    return response


@router.get("/exe", tags=["Files"])
@router.post("/exe", tags=["Files"])
@router.get("/exe/{path:path}", tags=["Files"])
@router.post("/exe/{path:path}", tags=["Files"])
def return_exe(path: str = None) -> StreamingResponse:
    """Return an EXE file containing random data."""

    if path is None:
        path = generate_random_name(".exe")
    elif not path.endswith(".exe"):
        path += ".exe"  # Add .exe extension if not present

    logger.info(f"Generating EXE file: {path}")

    # Create a simple EXE file structure in memory
    exe_content = (
        f"This is a random EXE file with random content: {fake.paragraph()}".encode(
            "utf-8"
        )
    )

    # Create a BytesIO buffer to hold the EXE file
    exe_buffer = BytesIO(exe_content)

    # Seek to the beginning of the BytesIO buffer
    exe_buffer.seek(0)

    # Create the StreamingResponse
    response = StreamingResponse(
        exe_buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={path}"},
    )

    logger.info("EXE file generated successfully.")

    return response
