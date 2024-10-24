from fastapi import APIRouter, Depends, HTTPException
from handlers.activities_handler import main as activity_main
from utils.dependencies import decode_jwt
from langchain_community.chat_models import ChatOllama
import app_logging

router = APIRouter()
logger = app_logging.setup_logger(__name__)

# Global lists to store documents
docs = []
documents = []


@router.post("/activity")  # Set the route to /activity
async def activity(query: str, username: str = Depends(decode_jwt)):
    global docs, documents

    # Log the incoming activity request
    logger.info(f"Processing activity request for user: {username} with query: {query}")

    # Initialize the ChatOllama model for activity
    llm = ChatOllama(model="activity", temperature=0.9)

    try:
        # Call the activity handler's main function and get the response
        response, docs, documents = activity_main(query, docs, documents)

        # Generate a response using the LLM
        llm_response = llm.invoke(query).content

        # Log the generated LLM response
        logger.debug(f"Activity response for {username}: {llm_response}")

        # Return the response in a JSON format
        return {"response": llm_response}

    except Exception as e:
        logger.error(f"Error processing activity for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
