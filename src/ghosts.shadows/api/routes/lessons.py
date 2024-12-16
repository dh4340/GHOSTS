from typing import Any

from app_logging import setup_logger
from config.config import LESSONS_MODEL
from fastapi import APIRouter, Depends, HTTPException
from handlers.handler import main as lessons_main
from utils.dependencies import Request, decode_jwt

router = APIRouter()
logger = setup_logger(__name__)

lesson_documents: list = []


@router.post("/lessons")
async def lessons(
    request: Request, username: str = Depends(decode_jwt)
) -> dict[str, Any]:
    """
    Process a lessons request from the user.

    Args:
        request (Request): The incoming request containing query parameters.
        username (str): The username extracted from the JWT token.

    Returns:
        dict[str, Any]: A JSON response containing the LLM's lessons response.
    """
    global lesson_documents
    query = request.query

    logger.info(f"Processing lessons request for user: {username} with query: {query}")

    if not query:
        logger.warning("Empty query received for lessons request.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response = lessons_main(query, lesson_documents, LESSONS_MODEL)
        logger.debug(f"Lessons response generated for {username}: {response}")

        return {"message": response}

    except Exception as e:
        logger.error(
            f"Error processing content for {username}: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
