import pytest
import requests
from requests.exceptions import Timeout, RequestException
from unittest.mock import patch

from utils.ollama import generate_document_with_ollama

@pytest.fixture
def mock_ollama_url():
    return "http://mock-ollama-api.com"

@pytest.fixture
def mock_ollama_timeout():
    return 5

@pytest.fixture
def example_prompt():
    return "Generate a sample document."

@pytest.fixture
def example_model():
    return "example-model"

def test_generate_document_with_ollama_success(
    requests_mock, mock_ollama_url, example_prompt, example_model, mock_ollama_timeout
):
    """Test successful generation with a valid response."""
    response_data = {"response": "This is a generated document."}
    requests_mock.post(mock_ollama_url, json=response_data, status_code=200)

    with patch("utils.ollama.OLLAMA_API_URL", mock_ollama_url):
        result = generate_document_with_ollama(example_prompt, example_model, mock_ollama_timeout)

    assert result == response_data["response"]


def test_generate_document_with_ollama_timeout(
    requests_mock, mock_ollama_url, example_prompt, example_model, mock_ollama_timeout
):
    """Test timeout handling."""
    requests_mock.post(mock_ollama_url, exc=Timeout)

    with patch("utils.ollama.OLLAMA_API_URL", mock_ollama_url):
        result = generate_document_with_ollama(example_prompt, example_model, mock_ollama_timeout)

    assert result is None


def test_generate_document_with_ollama_non_200_response(
    requests_mock, mock_ollama_url, example_prompt, example_model, mock_ollama_timeout
):
    """Test handling of non-200 HTTP responses."""
    requests_mock.post(mock_ollama_url, text="Internal Server Error", status_code=500)

    with patch("utils.ollama.OLLAMA_API_URL", mock_ollama_url):
        result = generate_document_with_ollama(example_prompt, example_model, mock_ollama_timeout)

    assert result is None


def test_generate_document_with_ollama_request_exception(
    requests_mock, mock_ollama_url, example_prompt, example_model, mock_ollama_timeout
):
    """Test handling of generic request exceptions."""
    requests_mock.post(mock_ollama_url, exc=RequestException("Connection Error"))

    with patch("utils.ollama.OLLAMA_API_URL", mock_ollama_url):
        result = generate_document_with_ollama(example_prompt, example_model, mock_ollama_timeout)

    assert result is None


def test_generate_document_with_ollama_unexpected_exception(
    mock_ollama_url, example_prompt, example_model, mock_ollama_timeout
):
    """Test handling of unexpected exceptions."""
    with patch("utils.ollama.OLLAMA_API_URL", mock_ollama_url), patch(
        "utils.ollama.requests.post", side_effect=Exception("Unexpected Error")
    ):
        result = generate_document_with_ollama(example_prompt, example_model, mock_ollama_timeout)

    assert result is None
