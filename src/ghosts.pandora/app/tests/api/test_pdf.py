from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_pdf_generation_success():
    """Test successful PDF generation."""
    response = client.get("/pdf")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    assert response.content  # Ensure content is returned


def test_pdf_custom_paragraphs():
    """Test PDF generation with custom paragraph count."""
    response = client.get("/pdf?num_paragraphs=10")
    assert response.status_code == 200
    # If the number of paragraphs is returned in the PDF (check body or content for validation)
    # Here you can inspect the PDF response content for validation, or check for length
    assert response.content  # Ensure content is returned
    assert len(response.content) > 0  # Ensure content length is more than 0


def test_pdf_invalid_paragraph_count():
    """Test PDF generation with invalid paragraph count."""
    response = client.get("/pdf?num_paragraphs=0")
    assert response.status_code == 422  # Validation error
