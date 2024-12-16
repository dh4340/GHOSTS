from typing import Any

from app_logging import setup_logger
from config.config import CHAT_MODEL
from fastapi import APIRouter, Depends, HTTPException
from handlers.llm_utils import generate_response
from utils.dependencies import Request, decode_jwt

router = APIRouter()
logger = setup_logger(__name__, level=10)


@router.post("/chat")
async def chat(request: Request, username: str = Depends(decode_jwt)) -> dict[str, Any]:
    """
    Process a chat request from the user.

    Args:
        request (Request): The incoming request containing query parameters.
        username (str): The username extracted from the JWT token.

    Returns:
        dict: A JSON response containing the LLM's chat response.
    """
    query = request.query
    logger.info(f"Processing chat request for user: {username} with query: {query}")

    if not query:
        logger.warning(f"Empty query received from user: {username}")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        logger.debug(f"Sending request to Ollama API with model: {CHAT_MODEL}")
        filtered_llm_response = generate_response(query, CHAT_MODEL)

        return {"message": filtered_llm_response}

    except Exception as e:
        logger.error(
            f"Unexpected error occurred while processing chat for {username}: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")
