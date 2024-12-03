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
            "word1, word2, word3"  # Mock AI-generated content for each row
        )
        yield mock_func


@pytest.fixture
def mock_generate_random_name():
    """Fixture to mock generate_random_name to avoid random file generation."""
    with patch("utils.helper.generate_random_name") as mock_func:
        mock_func.return_value = "test_file.xlsx"  # Mocked file name
        yield mock_func


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


def test_return_xlsx(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_enabled
):
    """Test the /sheets route with Ollama enabled and content generated using AI."""
    response = client.get("/sheets")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        "Content-Disposition" in response.headers
    )  # Ensure the filename is in the response header
    assert response.content  # Ensure that content is returned

    mock_generate_document_with_ollama.assert_called()  # Ensure Ollama was called
    mock_generate_random_name.assert_called_once()  # Ensure random file name was generated


def test_return_xlsx_with_custom_file_name(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_enabled
):
    """Test the /sheets/{file_name} route with a custom file name."""
    response = client.get("/sheets/custom_file.xlsx")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_file.xlsx"
    )
    assert response.content  # Ensure that content is returned

    mock_generate_document_with_ollama.assert_called()  # Ensure Ollama was called
    mock_generate_random_name.assert_not_called()  # Ensure random name wasn't generated


def test_return_xlsx_with_ollama_disabled(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_disabled
):
    """Test the /sheets route when Ollama is disabled."""
    response = client.get("/sheets")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        "Content-Disposition" in response.headers
    )  # Ensure the filename is in the response header
    assert response.content  # Ensure that content is returned

    mock_generate_document_with_ollama.assert_not_called()  # Ensure Ollama was not called
    mock_generate_random_name.assert_called_once()  # Ensure random file name was generated


def test_fallback_to_faker(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_enabled
):
    """Test that Faker is used when Ollama fails to generate content."""
    with patch(
        "utils.ollama.generate_document_with_ollama", side_effect=Exception("AI Error")
    ):
        response = client.get("/sheets")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        "Content-Disposition" in response.headers
    )  # Ensure the filename is in the response header
    assert response.content  # Ensure that content is returned

    mock_generate_document_with_ollama.assert_called()  # Ensure Ollama was called
    mock_generate_random_name.assert_called_once()  # Ensure random file name was generated


def test_invalid_file_extension(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_enabled
):
    """Test that invalid file extensions are corrected to .xlsx."""
    response = client.get("/sheets/custom_file.txt")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_file.xlsx"
    )
    assert response.content  # Ensure that content is returned

    mock_generate_document_with_ollama.assert_called()  # Ensure Ollama was called
    mock_generate_random_name.assert_not_called()  # Ensure random name wasn't generated


def test_generate_xlsx_with_random_data(
    mock_generate_document_with_ollama, mock_generate_random_name, mock_ollama_enabled
):
    """Test the random data generation logic (rows of data)."""
    response = client.get("/sheets")

    assert response.status_code == 200
    assert (
        response.headers["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert (
        len(response.content) > 0
    )  # Check if content is not empty (i.e., a valid Excel file is generated)

    # Additional checks could involve checking if rows are generated in the file, but here we just ensure non-emptiness
    mock_generate_document_with_ollama.assert_called()  # Ensure Ollama was called for row generation
