import io
import os
import time
import uuid

from app_logging import setup_logger
from fastapi.responses import StreamingResponse
from imaginairy.api import imagine
from imaginairy.schema import ImaginePrompt

logger = setup_logger(__name__)


def main(prompt: str) -> StreamingResponse:
    """
    Generates an image based on the provided prompt, saves it to disk with a unique filename,
    and returns it as an HTTP response.

    Args:
        prompt (str): The prompt used to generate the image.

    Returns:
        StreamingResponse: The image is returned as a streaming HTTP response.
    """
    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4()}.jpg"
    output_directory = "output_images"

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)
        logger.debug(f"Created output directory at {output_directory}")

    try:
        logger.info(f"Generating image for prompt: '{prompt}'")
        logger.debug(f"Prompt received: {prompt}")

        # Create an ImaginePrompt object
        imagine_prompt = ImaginePrompt(prompt, seed=1, model_weights="sdxl", size="hd")

        # Start time tracking for performance
        start_time = time.time()

        # Generate the image using Imaginairy's API
        for result in imagine([imagine_prompt]):
            output_path = os.path.join(output_directory, unique_filename)
            result.save(output_path)
            logger.info(f"Image successfully saved as '{output_path}'.")

        end_time = time.time()
        logger.info(
            f"Image generation completed in {end_time - start_time:.2f} seconds."
        )

        # Open the image file for sending in the response
        logger.debug(f"Opening image file for response: {output_path}")
        with open(output_path, "rb") as f:
            img_byte_array = f.read()

        # Return the image as a StreamingResponse
        logger.debug("Returning image as response.")
        return StreamingResponse(io.BytesIO(img_byte_array), media_type="image/jpeg")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Return an appropriate response in case of an error
        return {"error": f"An error occurred: {e}"}
