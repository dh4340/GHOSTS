import os
import random
import tempfile
import zipfile
from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
import app_logging
from faker import Faker
from utils.helper import generate_random_name
from utils.ollama import generate_document_with_ollama
from config.config import OLLAMA_ENABLED

# Setup logging
logger = app_logging.setup_logger("app_logger")

# Initialize Faker for fallback content generation
fake = Faker()

# Define the model name for Ollama
model = "llama3.2"

# Initialize FastAPI router
router = APIRouter()


@router.get("/chm", tags=["Web"])
@router.post("/chm", tags=["Web"])
@router.get("/chm/{file_name}", tags=["Web"])
@router.post("/chm/{file_name}", tags=["Web"])
def return_chm(file_name: str = None) -> StreamingResponse:
    """Return a CHM file containing random or Ollama-generated HTML content."""

    if file_name is None:
        file_name = generate_random_name(".chm")
    elif not file_name.endswith(".chm"):
        file_name += ".chm"  # Add .chm extension if not present

    logger.info(f"Generating CHM file: {file_name}")

    # Use a temporary directory to store HTML content
    with tempfile.TemporaryDirectory() as temp_dir:
        index_file_path = os.path.join(temp_dir, "index.html")

        # Prepare content using Ollama if enabled
        content_list = []
        if OLLAMA_ENABLED:
            try:
                # Use Ollama to generate document content
                prompt = (
                    "Create a series of HTML pages with interesting random content."
                )
                generated_content = generate_document_with_ollama(prompt, model)

                if generated_content:
                    content_list = generated_content.split(
                        "\n\n"
                    )  # Split by paragraphs
                    logger.info("Content generated successfully using Ollama.")
            except Exception as e:
                logger.error(f"Error using Ollama: {str(e)}")

        # Fallback to Faker if Ollama is not enabled or fails
        if not content_list:
            logger.info("Falling back to Faker for content generation.")
            content_list = [fake.paragraph() for _ in range(5)]

        # Write the index HTML file
        with open(index_file_path, "w", encoding="utf-8") as index_file:
            index_file.write("<html><head><title>Random CHM</title></head><body>")
            index_file.write("<h1>Random CHM Content</h1>")
            index_file.write("<ul>")

            # Create individual HTML pages
            for content in content_list:
                random_page_name = generate_random_name(".html")
                page_path = os.path.join(temp_dir, random_page_name)

                with open(page_path, "w", encoding="utf-8") as page_file:
                    page_file.write(
                        "<html><head><title>Random Page</title></head><body>"
                    )
                    page_file.write(f"<h2>{random_page_name}</h2>")
                    page_file.write(f"<p>{content}</p>")
                    page_file.write("</body></html>")

                index_file.write(
                    f'<li><a href="{random_page_name}">{random_page_name}</a></li>'
                )

            index_file.write("</ul>")
            index_file.write("</body></html>")

        # Create CHM file as a ZIP archive
        chm_buffer = BytesIO()
        with zipfile.ZipFile(chm_buffer, "w", zipfile.ZIP_DEFLATED) as chm_zip:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    chm_zip.write(file_path, arcname=file)

        # Seek to the beginning of the BytesIO buffer
        chm_buffer.seek(0)

        # Create and return the StreamingResponse
        response = StreamingResponse(
            chm_buffer,
            media_type="application/x-chm",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )

    logger.info("CHM file generated successfully.")
    return response


@router.get("/", tags=["Information"])
@router.get("/html", tags=["Web"])
@router.post("/html", tags=["Web"])
@router.get("/html/{file_name}", tags=["Web"])
@router.post("/html/{file_name}", tags=["Web"])
def return_html(file_name: str = None) -> HTMLResponse:
    """Return a random HTML file with content generated by Ollama or Faker."""

    if file_name is None:
        file_name = generate_random_name(".html")
    elif not file_name.endswith(".html"):
        file_name += ".html"

    logger.info(f"Generating HTML file: {file_name}")

    # Try to generate content with Ollama
    content = ""
    if OLLAMA_ENABLED:
        try:
            prompt = f"Generate an HTML document based using the following prompt '{file_name}' with several sections of rich content, your response should only contain the html and any inline css or javascript. No commentary is required."
            content = generate_document_with_ollama(prompt, model)

            if content:
                logger.info("HTML content generated successfully using Ollama.")
        except Exception as e:
            logger.error(f"Error using Ollama: {str(e)}")

    # Fallback to Faker if Ollama content is not available
    if not content:
        logger.info("Falling back to Faker for HTML content generation.")

        title = fake.text()
        body = "".join(
            [
                f"<h3>{fake.sentence().replace('.', '')}</h3>"
                + f"<p>{fake.paragraph(nb_sentences=random.randint(1, 100))}</p>"
                for _ in range(random.randint(1, 20))
            ]
        )
        header = f'<script type="text/javascript" src="/scripts/{fake.uuid4()}.js"></script><link rel="stylesheet" href="/css/{fake.uuid4()}/{fake.word()}.css" type="text/css" />'
        content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {header}
            <title>{title}</title>
        </head>
        <body>
            {body}
        </body>
        </html>
        """

    # Create and return the HTML response
    response = HTMLResponse(content=content)
    logger.info("HTML file generated successfully.")
    return response
