from typing import Any

from app_logging import setup_logger
from config.config import ACTIVITY_MODEL
from fastapi import APIRouter, Depends, HTTPException
from handlers.handler import main as activity_main
from utils.dependencies import Request, decode_jwt

activity_documents: list = []

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/activity")
async def activity(
    request: Request, username: str = Depends(decode_jwt)
) -> dict[str, Any]:
    """
    Process an activity request from the user.

    Args:
        request (Request): The incoming request containing query parameters.
        username (str): The username extracted from the JWT token.

    Returns:
        dict: A JSON response containing the filtered LLM response.
    """
    global activity_documents
    query = request.query

    logger.info(f"Processing activity request for user: {username} with query: {query}")

    if not query:
        logger.warning("Empty query received for lessons request.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        logger.debug(f"About to call activity_main with query: {query}")
        response = activity_main(query, activity_documents, ACTIVITY_MODEL)

        return {"message": response}

    except Exception as e:
        logger.error(
            f"Error processing activity for {username}: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
