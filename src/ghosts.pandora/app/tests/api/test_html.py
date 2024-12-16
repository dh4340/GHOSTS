from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_return_chm_with_default_filename(mock_random_name, mock_paragraph):
    response = client.get("/chm/")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=mock_file.chm"
    )
    assert response.headers["Content-Type"] == "application/x-chm"
    assert b"Mocked content" in response.content


def test_return_chm_with_custom_filename(mock_paragraph):
    response = client.get("/chm/custom_filename")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_filename.chm"
    )
    assert response.headers["Content-Type"] == "application/x-chm"
    assert b"Mocked content" in response.content


def test_return_html_with_default_filename(
    mock_random_name, mock_paragraph, mock_sentence
):
    response = client.get("/html/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "mock paragraph" in response.text.lower()
    assert "mock title" in response.text.lower()


def test_return_html_with_custom_filename(mock_paragraph, mock_sentence):
    response = client.get("/html/custom_page")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "mock paragraph" in response.text.lower()
    assert "mock title" in response.text.lower()
