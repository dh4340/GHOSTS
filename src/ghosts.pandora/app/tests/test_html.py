import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_random_name():
    """Fixture to mock random name generation."""
    with patch("utils.helper.generate_random_name") as mock_generate_random_name:
        mock_generate_random_name.return_value = "mock_file"
        yield mock_generate_random_name


@pytest.fixture
def mock_paragraph():
    """Fixture to mock Faker's paragraph generation."""
    with patch("faker.Faker.paragraph") as mock_paragraph:
        mock_paragraph.side_effect = [f"Mocked content {i}" for i in range(10)]
        yield mock_paragraph


@pytest.fixture
def mock_sentence():
    """Fixture to mock Faker's sentence generation."""
    with patch("faker.Faker.sentence") as mock_sentence:
        mock_sentence.side_effect = [f"Mock title {i}" for i in range(10)]
        yield mock_sentence


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
