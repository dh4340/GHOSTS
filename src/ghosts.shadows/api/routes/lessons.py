from fastapi import APIRouter, Depends, HTTPException
from handlers.lessons_handler import (
    main as lessons_main,
)  # Adjust the import to your lessons handler
from utils.dependencies import decode_jwt
from langchain_community.chat_models import ChatOllama
import app_logging

from typing import Any


router = APIRouter()
logger = app_logging.setup_logger(__name__)

# Global lists to store lesson documents
lesson_docs = []
lesson_documents = []


@router.post("/lessons")  # Set the route to /lessons
async def lessons(query: str, username: str = Depends(decode_jwt)) -> dict[str, Any]:
    global lesson_docs, lesson_documents

    # Log the incoming lessons request
    logger.info(f"Processing lessons request for user: {username} with query: {query}")

    # Initialize the ChatOllama model for lesson generation
    llm = ChatOllama(model="lessons", temperature=0.9)

    try:
        # Call the lessons handler's main function and get the response
        response, lesson_docs, lesson_documents = lessons_main(
            query, lesson_docs, lesson_documents
        )

        # Generate a response using the LLM
        llm_response = llm.invoke(query).content

        # Log the generated LLM response
        logger.debug(f"Lessons response for {username}: {llm_response}")

        # Return the response in a JSON format
        return {"response": llm_response}

    except Exception as e:
        logger.error(f"Error processing lessons for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
