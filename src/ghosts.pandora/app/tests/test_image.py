import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from io import BytesIO
from fastapi import Response
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_generate_image():
    """Fixture to mock the image generation function."""
    with patch("utils.text2image.generate_image_with_diffusers") as mock:
        yield mock


@pytest.fixture
def mock_ollama():
    """Fixture to mock Ollama's prompt generation."""
    with patch("utils.ollama.generate_document_with_ollama") as mock:
        yield mock


@pytest.fixture
def mock_fallback_image():
    """Fixture to mock the fallback image response."""
    with patch("utils.helper.generate_image_response") as mock:
        yield mock


def test_return_random_image_success(mock_generate_image):
    # Mock successful image generation
    mock_image_data = BytesIO(b"fake_image_data")
    mock_generate_image.return_value = mock_image_data

    response = client.get("/i")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")
    assert response.content == b"fake_image_data"


def test_return_random_image_fallback(mock_generate_image, mock_fallback_image):
    # Simulate a failure in image generation
    mock_generate_image.return_value = None
    mock_fallback_image.return_value = Response(
        content=b"fallback_image", media_type="image/png"
    )

    response = client.get("/i")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.content == b"fallback_image"


def test_return_image_with_ollama(mock_ollama, mock_generate_image):
    # Mock Ollama and image generation
    mock_ollama.return_value = "Enhanced prompt for testing"
    mock_image_data = BytesIO(b"generated_image_data")
    mock_generate_image.return_value = mock_image_data

    response = client.get("/i/sunset.jpg")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
    assert response.content == b"generated_image_data"
    mock_ollama.assert_called_once_with(
        "Based on the following text 'sunset', create a detailed and prompt for generating a high-quality images..."
    )


def test_return_image_invalid_format(mock_generate_image):
    # Test invalid image format handling
    response = client.get("/i/sunset.invalid")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/jpeg"
