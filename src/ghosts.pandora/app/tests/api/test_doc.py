import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Mock data
mock_doc_content = b"Mocked Word document content."
mock_ai_generated_content = "AI-generated content for the document."
mock_faker_content = "Faker-generated content for the document."
mock_file_name = "test_file.docx"


@pytest.fixture
def mock_generate_document_with_ollama():
    with patch("utils.ollama.generate_document_with_ollama") as mock:
        yield mock


@pytest.fixture
def mock_faker_paragraph():
    with patch("faker.Faker.paragraph") as mock:
        yield mock


@pytest.fixture
def mock_ollama_enabled():
    with patch("config.config.OLLAMA_ENABLED", True):
        yield


@pytest.fixture
def mock_ollama_disabled():
    with patch("config.config.OLLAMA_ENABLED", False):
        yield


@pytest.fixture
def mock_allowed_extensions():
    with patch("config.config.allowed_extensions", [".docx", ".doc", ".dot"]):
        yield


def test_return_doc_with_valid_filename_ollama_enabled(
    mock_ollama_enabled, mock_generate_document_with_ollama
):
    # Mock AI response
    mock_generate_document_with_ollama.return_value = mock_ai_generated_content

    # Test GET request with valid filename
    response = client.get(f"/doc/{mock_file_name}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == f"inline; filename={mock_file_name}"
    )
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    mock_generate_document_with_ollama.assert_called_once()


def test_return_doc_with_valid_filename_ollama_disabled(
    mock_ollama_disabled, mock_faker_paragraph
):
    # Mock Faker response
    mock_faker_paragraph.return_value = mock_faker_content

    # Test GET request with valid filename
    response = client.get(f"/doc/{mock_file_name}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == f"inline; filename={mock_file_name}"
    )
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    mock_faker_paragraph.assert_called_once()


def test_return_doc_with_invalid_filename(mock_allowed_extensions):
    # Test GET request with invalid filename
    invalid_file_name = "test_file.txt"
    response = client.get(f"/doc/{invalid_file_name}")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid file extension. Allowed extensions are: .docx, .doc, .dot"
    }


def test_return_doc_without_filename_ollama_enabled(
    mock_ollama_enabled, mock_generate_document_with_ollama
):
    # Mock AI response
    mock_generate_document_with_ollama.return_value = mock_ai_generated_content

    # Test GET request without filename
    response = client.get("/doc/")
    assert response.status_code == 200
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    assert response.headers["Content-Disposition"].endswith(".docx")
    mock_generate_document_with_ollama.assert_called_once()


def test_return_doc_without_filename_ollama_disabled(
    mock_ollama_disabled, mock_faker_paragraph
):
    # Mock Faker response
    mock_faker_paragraph.return_value = mock_faker_content

    # Test GET request without filename
    response = client.get("/doc/")
    assert response.status_code == 200
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    assert response.headers["Content-Disposition"].endswith(".docx")
    mock_faker_paragraph.assert_called_once()


def test_return_doc_with_fallback_to_faker_on_ollama_error(
    mock_ollama_enabled, mock_generate_document_with_ollama, mock_faker_paragraph
):
    # Mock Ollama to raise an exception
    mock_generate_document_with_ollama.side_effect = Exception("Ollama error")
    mock_faker_paragraph.return_value = mock_faker_content

    # Test GET request
    response = client.get(f"/doc/{mock_file_name}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == f"inline; filename={mock_file_name}"
    )
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    mock_generate_document_with_ollama.assert_called_once()
    mock_faker_paragraph.assert_called_once()
