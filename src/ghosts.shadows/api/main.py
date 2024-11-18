import os
from typing import Any

import app_logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    activity,
    chat,
    excel_content,
    image_content,
    lessons,
    social,
    web_content,
)

# Initialize logging
logger = app_logging.setup_logger(__name__)

# FastAPI app
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:7860",
    "http://0.0.0.0:7860",
    "http://*",
    "*",
    # Add other origins here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from different modules
app.include_router(activity.router)
app.include_router(chat.router)
app.include_router(web_content.router)
app.include_router(image_content.router)
app.include_router(excel_content.router)
app.include_router(lessons.router)
app.include_router(social.router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict[str, str]: A JSON response with a welcome message.
    """
    logger.debug("Root endpoint called")
    return {"message": "Welcome to the GHOSTS SHADOWS API"}


# Exception handling middleware
@app.middleware("http")
async def log_exceptions(request: Request, call_next) -> Any:
    """
    Middleware to log exceptions that occur during request processing.

    Args:
        request (Request): The incoming request.
        call_next: The next callable that processes the request.

    Returns:
        Any: The response from the next callable.
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exception:
        logger.error(
            f"HTTP Exception: {http_exception.detail} for path: {request.url.path}"
        )
        raise http_exception
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)} for path: {request.url.path}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn

    logger.info("GHOSTS SHADOWS coming online...")

    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    logger.debug(f"Ollama host set to: {ollama_host}")
    uvicorn.run("main:app", host="0.0.0.0", port=5900, reload=True)
