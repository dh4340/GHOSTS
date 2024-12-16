import os
import time
import uuid
from unittest.mock import patch

import config.config
import pytest
from app.main import app
from faker import Faker
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    """
    Fixture to provide a FastAPI test client.
    This client is shared across multiple tests within a session.
    """
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_proxy_env_vars():
    """
    Ensure that proxy environment variables are unset before each test.
    This mimics the behaviour in `main.py`.
    """
    env_vars_to_unset = ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]
    original_values = {var: os.environ.pop(var, None) for var in env_vars_to_unset}

    yield

    # Restore original values after the test
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value


@pytest.fixture(scope="function")
def mock_config(mocker):
    """
    Mock the app configuration settings for tests.
    """
    config_mock = mocker.patch("config.config")
    config_mock.OLLAMA_API_URL = "http://mocked-ollama-url"
    config_mock.OLLAMA_TIMEOUT = 1
    config_mock.LOG_LEVEL = "INFO"
    return config_mock


@pytest.fixture(scope="module")
def app_config():
    """
    Fixture to provide access to the configuration module.
    """
    return config.config


@pytest.fixture
def mock_generate_frames(mocker):
    """Fixture to mock the generate_frames function used in live_stream."""
    frame_count = 0
    max_frames = 10
    start_time = time.time()
    timeout = 10  # seconds

    def generate_frames():
        nonlocal frame_count
        while time.time() - start_time < timeout:
            yield b"frame"
            frame_count += 1
            if frame_count >= max_frames:
                break
        if frame_count < max_frames:
            raise AssertionError(
                f"Only {frame_count} frames generated within {timeout} seconds."
            )

    return mocker.patch("utils.helper.generate_frames", return_value=generate_frames())


@pytest.fixture
def mock_generate_video_with_cogvideox():
    """Fixture to mock the video generation function."""
    with patch("utils.text2video.generate_video_with_cogvideox") as mock_func:
        mock_func.return_value = "generated_video.mp4"
        yield mock_func


@pytest.fixture
def mock_os_path_isfile():
    """Fixture to mock os.path.isfile to simulate video file existence."""
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = True
        yield mock_isfile


@pytest.fixture
def mock_video_generation_disabled():
    """Fixture to simulate that video generation is disabled."""
    with patch("config.config.VIDEO_GENERATION_ENABLED", False):
        yield


@pytest.fixture
def mock_generate_document_with_ollama():
    """Fixture to mock the generate_document_with_ollama function."""
    with patch("utils.ollama.generate_document_with_ollama") as mock_func:
        mock_func.return_value = "actor1: Hello!\nactor2: Hi there!"
        yield mock_func


@pytest.fixture
def mock_generate_audio_response():
    """Fixture to mock the generate_audio_response function."""
    with patch("utils.voice.generate_audio_response") as mock_func:
        mock_func.return_value = b"fake_audio_data"
        yield mock_func


@pytest.fixture
def mock_create_temp_audio_file():
    """Fixture to mock create_temp_audio_file to avoid actual file creation."""
    with patch("utils.voice.create_temp_audio_file") as mock_func:
        mock_func.return_value = "/fake/path/to/audio.wav"
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


@pytest.fixture
def mock_random_name():
    """Fixture to mock random name generation."""
    with patch("utils.helper.generate_random_name") as mock_generate_random_name:
        mock_generate_random_name.return_value = "mock_file.txt"
        yield mock_generate_random_name


@pytest.fixture
def mock_ollama_enabled():
    """Fixture to simulate that Ollama is enabled."""
    with patch("config.config.OLLAMA_ENABLED", True):
        yield


@pytest.fixture
def mock_ollama_disabled():
    """Fixture to simulate that Ollama is disabled."""
    with patch("config.config.OLLAMA_ENABLED", False):
        yield


@pytest.fixture
def mock_allowed_extensions():
    with patch("config.config.allowed_extensions", [".docx", ".doc", ".dot"]):
        yield


@pytest.fixture
def mock_generate_archive_zip():
    with patch("utils.helper.generate_archive") as mock:
        yield mock


@pytest.fixture
def mock_generate_archive_tar():
    with patch("utils.helper.generate_archive") as mock:
        yield mock


@pytest.fixture
def mock_create_response():
    with patch("utils.helper.create_response") as mock:
        yield mock


@pytest.fixture
def mock_faker_paragraph():
    """Fixture to mock Faker's paragraph generation."""
    with patch.object(Faker(), "paragraph") as mock_paragraph:
        mock_paragraph.return_value = "Mocked paragraph."
        yield mock_paragraph


@pytest.fixture
def mock_faker_sentence():
    """Fixture to mock Faker's sentence generation."""
    with patch.object(Faker(), "sentence") as mock_sentence:
        mock_sentence.return_value = "Mocked sentence."
        yield mock_sentence


@pytest.fixture
def mock_fake_csv():
    """Fixture to mock Faker's CSV generation."""
    with patch.object(Faker(), "csv") as mock_csv:
        mock_csv.return_value = "mock,csv,data"
        yield mock_csv


@pytest.fixture
def custom_iso_filename():
    """
    Fixture for providing a custom ISO file name.
    This will be used for the test_return_iso_custom_name test.
    """
    return "custom_name.iso"


@pytest.fixture
def missing_extension_filename():
    """
    Fixture for providing a file name without the .iso extension.
    This will be used for the test_return_iso_missing_extension test.
    """
    return "file_without_extension"


@pytest.fixture
def mock_random_binary_length():
    with patch("utils.helper.generate_random_length") as mock:
        yield mock


@pytest.fixture
def mock_file_name(request):
    """Fixture to generate a unique mock file name based on file type."""

    def generate_mock_file_name(file_extension="txt"):
        return f"test_file_{uuid.uuid4().hex}.{file_extension}"

    return generate_mock_file_name


@pytest.fixture
def example_prompt():
    return "Write a detailed report about renewable energy."


@pytest.fixture
def example_model():
    return "gpt-3.5-turbo"


@pytest.fixture
def mock_ollama_url():
    return "https://api.example.com/ollama"


@pytest.fixture
def mock_ollama_timeout():
    return 10  # seconds
