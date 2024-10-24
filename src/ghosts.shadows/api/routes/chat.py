from fastapi import APIRouter, Depends, HTTPException
from utils.dependencies import decode_jwt
from langchain_community.chat_models import ChatOllama
import app_logging

router = APIRouter()
logger = app_logging.setup_logger(__name__)

# Global lists to store chat documents
chat_docs = []
chat_documents = []


@router.post("/chat")  # Set the route to /chat
async def chat(query: str, username: str = Depends(decode_jwt)):
    global chat_docs, chat_documents

    # Log the incoming chat request
    logger.info(f"Processing chat request for user: {username} with query: {query}")

    # Initialize the ChatOllama model for chat
    llm = ChatOllama(model="chat", temperature=0.9)

    try:
        # Generate a response using the LLM
        llm_response = llm.invoke(query).content

        # Log the generated LLM response
        logger.debug(f"Chat response for {username}: {llm_response}")

        # Return the response in a JSON format
        return {"response": llm_response}

    except Exception as e:
        logger.error(f"Error processing chat for {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
