from typing import Any

from app_logging import setup_logger
from config.config import EXCEL_CONTENT_MODEL
from fastapi import APIRouter, Depends, HTTPException
from handlers.handler import main as content_main
from utils.dependencies import Request, decode_jwt

router = APIRouter()
logger = setup_logger(__name__)

content_documents: list = []


@router.post("/excel_content")
async def content(
    request: Request, username: str = Depends(decode_jwt)
) -> dict[str, Any]:
    """
    Process a content request from the user.

    Args:
        request (Request): The incoming request containing query parameters.
        username (str): The username extracted from the JWT token.

    Returns:
        dict: A JSON response containing the LLM's content response.
    """
    global content_docs, content_documents
    query = request.query

    logger.info(f"Processing content request for user: {username} with query: {query}")

    if not query:
        logger.warning("Empty query received for lessons request.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response = content_main(query, content_documents, EXCEL_CONTENT_MODEL)
        logger.debug(f"Excel Content response for {username}: {response}")

        return {"message": response}

    except Exception as e:
        logger.error(
            f"Error processing content for {username}: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
