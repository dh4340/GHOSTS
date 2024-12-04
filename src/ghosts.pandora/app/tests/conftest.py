import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
import config.config


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
    config_mock.OLLAMA_TIMEOUT = 1  # Set a low timeout for testing purposes
    config_mock.LOG_LEVEL = "INFO"
    return config_mock

@pytest.fixture(scope="module")
def app_config():
    """
    Fixture to provide access to the configuration module.
    """
    return config
