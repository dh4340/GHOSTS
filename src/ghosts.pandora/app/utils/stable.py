import torch
from diffusers import StableDiffusionPipeline
import app_logging
import io
from config.config import STABLE_MODEL_FILE_PATH, STABLE_LOCAL_FILES_ONLY

# Setup logging
logger = app_logging.setup_logger(__name__)


def generate_image_with_diffusers(prompt: str):
    """Generate an image using the Stable Diffusion model and return it as bytes."""

    logger.info(
        "Requesting image generation with Stable Diffusion for prompt: %s", prompt
    )

    try:
        # Load the Stable Diffusion model
        pipeline = StableDiffusionPipeline.from_pretrained(
            STABLE_MODEL_FILE_PATH,
            torch_dtype=torch.float16,
            local_files_only=STABLE_LOCAL_FILES_ONLY,
        )
        # Move the model to GPU for faster inference
        pipeline = pipeline.to("cuda")

        # Generate the image
        image = pipeline(prompt=prompt).images[0]

        if image:
            logger.info("Image generated successfully.")
            # Convert the image to bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes = image_bytes.getvalue()
            return image_bytes
        else:
            logger.warning("No image generated.")
            return None
    except Exception as e:
        logger.error("Error generating image: %s", e)
        return None
