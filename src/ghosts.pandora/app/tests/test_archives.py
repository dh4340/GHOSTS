import pytest
from fastapi.testclient import TestClient
from app import main
from unittest.mock import patch

client = TestClient(main)

# Mock data for testing
mock_zip_data = b"Random binary data for zip"
mock_tar_data = b"Random binary data for tar"
mock_file_name = "test.zip"
mock_tar_file_name = "test.tar"


@pytest.fixture
def mock_generate_archive_zip():
    with patch("utils.helper.generate_archive") as mock:
        yield mock


@pytest.fixture
def mock_generate_archive_tar():
    with patch("utils.helper.generate_archive") as mock:
        yield mock


@pytest.fixture
def mock_create_response():
    with patch("utils.helper.create_response") as mock:
        yield mock


def test_return_zip(mock_generate_archive_zip, mock_create_response):
    # Mock the return value of the generate_archive function
    mock_generate_archive_zip.return_value = mock_zip_data
    mock_create_response.return_value = (
        mock_zip_data  # Assuming create_response returns the buffer directly
    )

    # Test GET request without file_name
    response = client.get("/zip")
    assert response.status_code == 200
    assert response.content == mock_zip_data

    # Test GET request with file_name
    response = client.get(f"/zip/{mock_file_name}")
    assert response.status_code == 200
    assert response.content == mock_zip_data
    mock_generate_archive_zip.assert_called_with(mock_file_name, "zip")


def test_return_tar(mock_generate_archive_tar, mock_create_response):
    # Mock the return value of the generate_archive function
    mock_generate_archive_tar.return_value = mock_tar_data
    mock_create_response.return_value = (
        mock_tar_data  # Assuming create_response returns the buffer directly
    )

    # Test GET request without file_name
    response = client.get("/tar")
    assert response.status_code == 200
    assert response.content == mock_tar_data

    # Test GET request with file_name
    response = client.get(f"/tar/{mock_tar_file_name}")
    assert response.status_code == 200
    assert response.content == mock_tar_data
    mock_generate_archive_tar.assert_called_with(mock_tar_file_name, "tar")


def test_post_return_zip(mock_generate_archive_zip, mock_create_response):
    # Mock the return value of the generate_archive function
    mock_generate_archive_zip.return_value = mock_zip_data
    mock_create_response.return_value = (
        mock_zip_data  # Assuming create_response returns the buffer directly
    )

    # Test POST request without file_name
    response = client.post("/zip")
    assert response.status_code == 200
    assert response.content == mock_zip_data

    # Test POST request with file_name
    response = client.post(f"/zip/{mock_file_name}")
    assert response.status_code == 200
    assert response.content == mock_zip_data
    mock_generate_archive_zip.assert_called_with(mock_file_name, "zip")


def test_post_return_tar(mock_generate_archive_tar, mock_create_response):
    # Mock the return value of the generate_archive function
    mock_generate_archive_tar.return_value = mock_tar_data
    mock_create_response.return_value = (
        mock_tar_data  # Assuming create_response returns the buffer directly
    )

    # Test POST request without file_name
    response = client.post("/tar")
    assert response.status_code == 200
    assert response.content == mock_tar_data

    # Test POST request with file_name
    response = client.post(f"/tar/{mock_tar_file_name}")
    assert response.status_code == 200
    assert response.content == mock_tar_data
    mock_generate_archive_tar.assert_called_with(mock_tar_file_name, "tar")
