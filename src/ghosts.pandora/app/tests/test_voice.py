import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_generate_document_with_ollama():
    """Fixture to mock the generate_document_with_ollama function."""
    with patch("utils.ollama.generate_document_with_ollama") as mock_func:
        mock_func.return_value = (
            "actor1: Hello!\nactor2: Hi there!"  # Mock the conversation script
        )
        yield mock_func


@pytest.fixture
def mock_generate_audio_response():
    """Fixture to mock the generate_audio_response function."""
    with patch("utils.voice.generate_audio_response") as mock_func:
        mock_func.return_value = b"fake_audio_data"  # Mock the audio data
        yield mock_func


@pytest.fixture
def mock_create_temp_audio_file():
    """Fixture to mock create_temp_audio_file to avoid actual file creation."""
    with patch("utils.voice.create_temp_audio_file") as mock_func:
        mock_func.return_value = "/fake/path/to/audio.wav"  # Mock file path
        yield mock_func


@pytest.fixture
def mock_voice_generation_enabled():
    """Fixture to simulate that voice generation is enabled."""
    with patch("config.config.VOICE_GENERATION_ENABLED", True):
        yield


@pytest.fixture
def mock_voice_generation_disabled():
    """Fixture to simulate that voice generation is disabled."""
    with patch("config.config.VOICE_GENERATION_ENABLED", False):
        yield


def test_generate_synthesised_conversation(
    mock_generate_document_with_ollama,
    mock_generate_audio_response,
    mock_create_temp_audio_file,
    mock_voice_generation_enabled,
):
    """Test the /call route with voice generation enabled."""
    response = client.get("/call")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/wav"
    assert (
        response.content == b"fake_audio_data"
    )  # Check if the audio content is returned

    mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
    mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called
    mock_create_temp_audio_file.assert_called_once()  # Ensure temp file creation was called


def test_generate_synthesised_conversation_text(
    mock_generate_document_with_ollama, mock_voice_generation_disabled
):
    """Test the /call route with voice generation disabled."""
    response = client.get("/call")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"
    assert (
        response.text == "actor1: Hello!\nactor2: Hi there!"
    )  # Check if the conversation script is returned as text

    mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called


def test_generate_synthesised_conversation_failure(mock_generate_document_with_ollama):
    """Test the /call route when script generation fails."""
    with patch("utils.ollama.generate_document_with_ollama", return_value=None):
        response = client.get("/call")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"
    assert (
        response.text == "Failed to generate conversation script."
    )  # Check if failure message is returned

    mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called


def test_audio_generation_failure(
    mock_generate_document_with_ollama, mock_generate_audio_response
):
    """Test the /call route when audio generation fails."""
    with patch("utils.voice.generate_audio_response", return_value=None):
        response = client.get("/call")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"
    assert (
        response.text == "Audio synthesis failed."
    )  # Check if failure message is returned

    mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
    mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called


def test_generate_synthesised_conversation_with_custom_actors(
    mock_generate_document_with_ollama,
    mock_generate_audio_response,
    mock_create_temp_audio_file,
    mock_voice_generation_enabled,
):
    """Test the /call route with custom actors."""
    response = client.get("/call?actor1=developer&actor2=manager")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/wav"
    assert (
        response.content == b"fake_audio_data"
    )  # Check if the audio content is returned

    mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
    mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called
    mock_create_temp_audio_file.assert_called_once()  # Ensure temp file creation was called
