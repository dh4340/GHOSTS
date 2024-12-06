import pytest
from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    "method, endpoint, custom_file_name, ollama_enabled, side_effect, expected_file_name, expected_random_name_calls, expected_ollama_calls",
    [
        # Test /sheets with Ollama enabled
        ("get", "/sheets", None, True, None, "random_file.xlsx", 1, 1),
        # Test /sheets/{file_name} with custom file name
        ("get", "/sheets/custom_file.xlsx", "custom_file.xlsx", True, None, "custom_file.xlsx", 0, 1),
        # Test /sheets with Ollama disabled
        ("get", "/sheets", None, False, None, "random_file.xlsx", 1, 0),
        # Test fallback to Faker when Ollama fails
        ("get", "/sheets", None, True, Exception("AI Error"), "random_file.xlsx", 1, 1),
        # Test invalid file extension correction
        ("get", "/sheets/custom_file.txt", "custom_file.txt", True, None, "custom_file.xlsx", 0, 1),
        # Test random data generation
        ("get", "/sheets", None, True, None, "random_file.xlsx", 1, 1),
    ],
)
@patch("app.helpers.generate_document_with_ollama")
@patch("app.helpers.generate_random_name")
def test_xlsx_endpoints(
    mock_random_name,
    mock_generate_document_with_ollama,
    monkeypatch,
    method,
    endpoint,
    custom_file_name,
    ollama_enabled,
    side_effect,
    expected_file_name,
    expected_random_name_calls,
    expected_ollama_calls,
):
    """Refactored test cases for all endpoints and configurations."""

    # Mock OLLAMA_ENABLED config
    monkeypatch.setattr("config.config.OLLAMA_ENABLED", ollama_enabled)

    # Set up mock return values
    mock_random_name.return_value = "random_file.xlsx"
    mock_generate_document_with_ollama.return_value = "word1, word2, word3"

    # Simulate an exception for Ollama if needed
    if side_effect:
        mock_generate_document_with_ollama.side_effect = side_effect

    # Call the endpoint using the specified HTTP method
    response = getattr(client, method)(endpoint)

    # Common assertions for all cases
    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "Content-Disposition" in response.headers
    assert response.content  # Ensure non-empty response content
    assert response.headers["Content-Disposition"].endswith(expected_file_name)

    # Verify the number of calls to mocks
    assert mock_random_name.call_count == expected_random_name_calls
    assert mock_generate_document_with_ollama.call_count == expected_ollama_calls
