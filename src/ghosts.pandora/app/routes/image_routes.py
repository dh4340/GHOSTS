from fastapi import APIRouter, Response
import random
from faker import Faker
from utils.helper import generate_image_response
import app_logging
from config.config import OLLAMA_ENABLED
from utils.stable import generate_image_with_diffusers

MODEL_NAME = "imagegen-v1"

logger = app_logging.setup_logger("app_logger")

fake = Faker()

router = APIRouter()


@router.get("/i", tags=["Image"])
@router.post("/i", tags=["Image"])
@router.get("/img", tags=["Image"])
@router.post("/img", tags=["Image"])
@router.get("/images", tags=["Image"])
@router.post("/images", tags=["Image"])
def return_random_image() -> Response:
    """Generate and return a random image if enabled."""
    request_type = random.choice(["jpg", "png", "gif"])

    if OLLAMA_ENABLED:
        # Define a prompt for the model
        prompt = "Generate a random image with vivid colors and an abstract design."
        logger.info("Requesting image generation with prompt: %s", prompt)

        # Generate the image
        image_data = generate_image_with_diffusers(prompt)

        if image_data:
            # Return the image data in the response
            return Response(content=image_data, media_type=f"image/{request_type}")
        else:
            logger.warning("Falling back to default image generation.")

    # Fallback to default image generation if Ollama is not enabled or fails
    return generate_image_response(request_type)


@router.get("/i/{path:path}", tags=["Image"])
@router.post("/i/{path:path}", tags=["Image"])
@router.get("/img/{path:path}", tags=["Image"])
@router.post("/img/{path:path}", tags=["Image"])
@router.get("/images/{path:path}", tags=["Image"])
@router.post("/images/{path:path}", tags=["Image"])
def return_image(path: str) -> Response:
    """Generate and return an image based on the request path, if enabled."""
    request_type = (
        path.split(".")[-1] if "." in path else random.choice(["jpg", "png", "gif"])
    )

    if request_type not in ["jpg", "png", "gif", "ico"]:
        logger.warning(
            f"Invalid image type requested: {request_type}. Defaulting to jpg."
        )
        request_type = "jpg"  # Default to jpg if invalid type is requested

    logger.info(f"Received request to generate image of type: {request_type}")

    if OLLAMA_ENABLED:
        # Define a prompt based on the path
        prompt = f"Generate an image representing {path}."
        logger.info("Requesting image generation with prompt: %s", prompt)

        # Generate the image using Ollama
        image_data = generate_image_with_diffusers(prompt)

        if image_data:
            # Return the image data in the response
            return Response(content=image_data, media_type=f"image/{request_type}")
        else:
            logger.warning("Falling back to default image generation.")

    # Fallback to default image generation if Ollama is not enabled or fails
    return generate_image_response(request_type)
