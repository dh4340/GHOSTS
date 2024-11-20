from typing import Any, Union

from app_logging import setup_logger
from config.config import IMAGE_CONTENT_MODEL
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from handlers.handler import main as content_main
from handlers.img_handler import main as image_handler
from utils.dependencies import Request, decode_jwt

router = APIRouter()
logger = setup_logger(__name__)

content_documents: list = []


@router.post("/image_content", response_model=None)
async def content(
    request: Request, username: str = Depends(decode_jwt)
) -> Union[dict[str, Any], StreamingResponse]:
    """
    Process a content request from the user.

    Args:
        request (Request): The incoming request containing query parameters.
        username (str): The username extracted from the JWT token.

    Returns:
        Union[dict, StreamingResponse]: A JSON response with text or a StreamingResponse with an image.
    """
    global content_documents
    query = request.query

    logger.info(f"Processing content request for user: {username} with query: {query}")

    if not query:
        logger.warning("Empty query received for lessons request.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        # Generate content response
        response = content_main(query, content_documents, IMAGE_CONTENT_MODEL)
        logger.debug(f"Content response for {username}: {response}")

        # Use image_handler to generate and return a StreamingResponse
        return image_handler(response)

    except Exception as e:
        logger.error(
            f"Error processing content for {username}: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
