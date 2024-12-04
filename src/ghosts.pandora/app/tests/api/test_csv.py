import pytest
from fastapi.testclient import TestClient
from app import main
from unittest.mock import patch
import random

client = TestClient(main)

# Mock data for testing
mock_csv_data = "Name,Address,Password\nJohn Doe,123 Fake St,secret\nJane Smith,456 Another St,secret2\n"
mock_file_name = "test_file"
mock_ollama_csv_data = (
    "Name,Address,Password\nOllama User,Generated Address,Generated Password\n"
)


@pytest.fixture
def mock_generate_document_with_ollama():
    with patch("utils.ollama.generate_document_with_ollama") as mock:
        yield mock


@pytest.fixture
def mock_fake_csv():
    with patch.object(random, "randint") as mock_randint:
        yield mock_randint


@pytest.fixture
def mock_faker_csv():
    with patch("faker.Faker.csv") as mock:
        yield mock


@pytest.fixture
def mock_ollama_enabled():
    with patch("config.config.OLLAMA_ENABLED", True):
        yield


@pytest.fixture
def mock_ollama_disabled():
    with patch("config.config.OLLAMA_ENABLED", False):
        yield


def test_return_csv_with_ollama_enabled(
    mock_ollama_enabled, mock_generate_document_with_ollama
):
    # Mock the return value of the Ollama model for CSV generation
    mock_generate_document_with_ollama.return_value = mock_ollama_csv_data

    # Test GET request with path
    response = client.get("/csv/test")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == mock_ollama_csv_data
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'
    mock_generate_document_with_ollama.assert_called_once_with(
        f"Generate a CSV document with {random.randint(1, 100)} rows of fake data. The columns should include Name, Address, and Password. The data should be realistic and varied.",
        "CSV_MODEL",
    )


def test_return_csv_with_ollama_disabled(mock_ollama_disabled, mock_faker_csv):
    # Mock the return value of Faker's CSV generation
    mock_faker_csv.return_value = mock_csv_data

    # Test GET request with path
    response = client.get("/csv/test")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == mock_csv_data
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'
    mock_faker_csv.assert_called_once()


def test_post_return_csv_with_ollama_enabled(
    mock_ollama_enabled, mock_generate_document_with_ollama
):
    # Mock the return value of the Ollama model for CSV generation
    mock_generate_document_with_ollama.return_value = mock_ollama_csv_data

    # Test POST request with path
    response = client.post("/csv/test")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == mock_ollama_csv_data
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'
    mock_generate_document_with_ollama.assert_called_once_with(
        f"Generate a CSV document with {random.randint(1, 100)} rows of fake data. The columns should include Name, Address, and Password. The data should be realistic and varied.",
        "CSV_MODEL",
    )


def test_post_return_csv_with_ollama_disabled(mock_ollama_disabled, mock_faker_csv):
    # Mock the return value of Faker's CSV generation
    mock_faker_csv.return_value = mock_csv_data

    # Test POST request with path
    response = client.post("/csv/test")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == mock_csv_data
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'
    mock_faker_csv.assert_called_once()


def test_return_csv_with_random_name(mock_ollama_disabled, mock_faker_csv):
    # Mock the return value of Faker's CSV generation
    mock_faker_csv.return_value = mock_csv_data

    # Test GET request with path None (random file name)
    response = client.get("/csv/")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == mock_csv_data
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"].endswith(".csv")
    mock_faker_csv.assert_called_once()
