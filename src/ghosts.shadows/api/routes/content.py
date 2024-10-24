from fastapi import APIRouter, Depends, HTTPException
from handlers.content_handler import (
    main as content_main,
)  # Adjust the import to your content handler
from utils.dependencies import decode_jwt
from langchain_community.chat_models import ChatOllama
import app_logging

router = APIRouter()
logger = app_logging.setup_logger(__name__)

# Global lists to store content documents
content_docs = []
content_documents = []


@router.post("/content")  # Set the route to /content
async def content(query: str, username: str = Depends(decode_jwt)):
    global content_docs, content_documents

    # Log the incoming content request
    logger.info(f"Processing content request for user: {username} with query: {query}")

    # Initialize the ChatOllama model for content generation
    llm = ChatOllama(model="web_content", temperature=0.9)

    try:
        # Call the content handler's main function and get the response
        response, content_docs, content_documents = content_main(
            query, content_docs, content_documents
        )

        # Generate a response using the LLM
        llm_response = llm.invoke(query).content

        # Log the generated LLM response
        logger.debug(f"Content response for {username}: {llm_response}")

        # Return the response in a JSON format
        return {"response": llm_response}

    except Exception as e:
        logger.error(f"Error processing content for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
