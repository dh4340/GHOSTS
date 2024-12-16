import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_with_valid_filename_ollama_enabled(method, mock_file_name):
    """Test valid filename with Ollama enabled."""
    file_name = mock_file_name("docx")
    response = getattr(client, method)(f"/doc/{file_name}")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f"inline; filename={file_name}"
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_with_valid_filename_ollama_disabled(method, mock_file_name):
    """Test valid filename with Ollama disabled."""
    file_name = mock_file_name("docx")
    response = getattr(client, method)(f"/doc/{file_name}")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f"inline; filename={file_name}"
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_with_invalid_filename(method):
    """Test invalid filename."""
    invalid_file_name = "test_file.txt"
    response = getattr(client, method)(f"/doc/{invalid_file_name}")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid file extension. Allowed extensions are: .doc, .docx, .dot, .dotx, .docm, .dotm, .odt"
    }


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_without_filename_ollama_enabled(method):
    """Test request without filename with Ollama enabled."""
    response = getattr(client, method)("/doc/")
    assert response.status_code == 200
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    assert response.headers["Content-Disposition"].endswith(".docx")


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_without_filename_ollama_disabled(method):
    """Test request without filename with Ollama disabled."""
    response = getattr(client, method)("/doc/")
    assert response.status_code == 200
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
    assert response.headers["Content-Disposition"].endswith(".docx")


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_doc_with_fallback_to_faker_on_ollama_error(method, mock_file_name):
    """Test fallback to Faker when Ollama fails."""
    file_name = mock_file_name("docx")
    response = getattr(client, method)(f"/doc/{file_name}")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == f"inline; filename={file_name}"
    assert (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        in response.headers["Content-Type"]
    )
