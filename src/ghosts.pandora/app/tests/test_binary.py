import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from faker import Faker
from app.main import app
import random

client = TestClient(app)

# Mock data for testing
mock_binary_data = b"Random binary data"
mock_file_name = "test_file.bin"


@pytest.fixture
def mock_generate_random_name():
    with patch("utils.helper.generate_random_name") as mock:
        yield mock


@pytest.fixture
def mock_random_binary_length():
    with patch("random.randint") as mock:
        yield mock


@pytest.fixture
def mock_binary():
    """Fixture to mock Faker's paragraph generation."""
    with patch.object(Faker(), "binary") as mock_binary_data:
        mock_binary_data.return_value = "Mocked binary."
        yield mock_binary_data


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_binary_without_file_name(
    method, mock_generate_random_name, mock_binary, mock_random_binary_length
):
    """Test binary file generation without a file name (GET and POST)."""
    mock_generate_random_name.return_value = mock_file_name
    mock_random_binary_length.return_value = 2000
    mock_binary.return_value = mock_binary_data

    response = getattr(client, method)("/binary")
    assert response.status_code == 200
    assert response.content == mock_binary_data
    assert (
        response.headers["Content-Disposition"]
        == f'attachment; filename={mock_file_name}'
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert len(response.content) == 2000

    mock_generate_random_name.assert_called_once_with(".bin")
    mock_random_binary_length.assert_called_once_with(1000, 3000000)


@pytest.mark.parametrize("method", ["get", "post"])
def test_return_binary_with_file_name(
    method, mock_binary, mock_random_binary_length
):
    """Test binary file generation with a file name (GET and POST)."""
    mock_random_binary_length.return_value = 1500
    mock_binary.return_value = mock_binary_data

    response = getattr(client, method)(f"/binary/{mock_file_name}")
    assert response.status_code == 200
    assert response.content == mock_binary_data
    assert (
        response.headers["Content-Disposition"]
        == f'attachment; filename={mock_file_name}'
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert len(response.content) == 1500

    mock_random_binary_length.assert_called_once_with(1000, 3000000)


def test_binary_file_logging(mock_generate_random_name, caplog):
    """Test logging for binary file generation."""
    mock_generate_random_name.return_value = mock_file_name

    with caplog.at_level("INFO"):
        response = client.get("/binary")
        assert response.status_code == 200
        assert "Generated random file name" in caplog.text
        assert f"Serving binary file: {mock_file_name}" in caplog.text
