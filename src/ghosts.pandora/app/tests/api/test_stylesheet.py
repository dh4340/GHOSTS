from app import main
from fastapi.testclient import TestClient

client = TestClient(main)


def test_return_stylesheet_success(default_stylesheet_response):
    """Test successful stylesheet generation with random styles."""
    response = default_stylesheet_response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/css"
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"] == "inline; filename=style.css"
    assert len(response.content) > 0  # Ensure content is returned


def test_return_stylesheet_with_ollama(ollama_stylesheet_response):
    """Test stylesheet generation with Ollama enabled."""
    response = ollama_stylesheet_response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/css"
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"] == "inline; filename=style.css"
    assert "font-family: Arial" in response.content.decode(
        "utf-8"
    )  # Verify Ollama output


def test_return_stylesheet_fallback(fallback_stylesheet_response):
    """Test stylesheet generation when Ollama is disabled or fails."""
    response = fallback_stylesheet_response
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/css"
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"] == "inline; filename=style.css"
    assert "font-family" in response.content.decode(
        "utf-8"
    )  # Ensure font is included in CSS


def test_return_stylesheet_invalid_data():
    """Test invalid path handling for stylesheet generation."""
    response = client.get("/stylesheet/invalidpath")
    assert response.status_code == 404  # Should trigger a 404 error for invalid paths


def test_stylesheet_content_structure(default_stylesheet_response):
    """Test the structure of the generated stylesheet content."""
    response = default_stylesheet_response
    assert response.status_code == 200
    css_content = response.content.decode("utf-8")

    # Check for general CSS structure
    assert "* {" in css_content  # Ensure body font-family rule exists
    assert "h1 {" in css_content  # Ensure h1 font-family rule exists
    assert "background-color" in css_content  # Ensure background-color is generated
    assert "font-size" in css_content  # Ensure font-size for p tags
