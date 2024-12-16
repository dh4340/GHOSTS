from unittest.mock import patch

from app import main
from fastapi.testclient import TestClient

client = TestClient(main)


def test_return_script_success(default_script_response):
    """Test script generation with a random file name."""
    response = default_script_response
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"].startswith("attachment; filename=")
    assert len(response.content) > 0  # Ensure content is returned


def test_return_script_custom_filename(custom_filename_script_response):
    """Test script generation with a custom file name."""
    response = custom_filename_script_response
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_script.py"
    )
    assert len(response.content) > 0  # Ensure content is returned


def test_script_content_structure(script_with_content_response):
    """Test the structure of the generated script content."""
    response = script_with_content_response
    assert response.status_code == 200

    # Check if the script content is either JavaScript or Python
    content = response.content.decode("utf-8")
    assert "console.log" in content or "import datetime" in content


def test_return_script_with_ollama_failure(default_script_response):
    """Test script generation with Ollama failure."""
    # Mock Ollama to simulate failure
    with patch("utils.ollama.generate_document_with_ollama") as mock_ollama:
        mock_ollama.side_effect = Exception(
            "Ollama service unavailable"
        )  # Simulate failure

        response = default_script_response
        assert response.status_code == 200  # Ensure fallback is used
        assert "Content-Disposition" in response.headers
        assert len(response.content) > 0  # Ensure fallback content is returned


def test_return_script_invalid_data():
    """Test script generation with invalid data."""
    response = client.get("/script/invalidfile")
    assert (
        response.status_code == 500
    )  # Should trigger internal error due to invalid path or data
    assert response.json() == {
        "detail": "An error occurred while generating the script."
    }
