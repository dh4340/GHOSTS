import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_random_name():
    """Fixture to mock the random name generation function."""
    with patch("utils.helper.generate_random_name") as mock_name:
        mock_name.return_value = "random_file.txt"
        yield mock_name


@pytest.fixture
def mock_endpoint_mapping():
    """Fixture to mock the endpoint mapping and the endpoint function."""
    with patch("routes.archive_routes.return_zip") as mock_func:
        mock_func.return_value = {"message": "Success"}
        yield mock_func


@pytest.fixture
def mock_valid_endpoints():
    """Fixture to mock valid endpoints."""
    with patch("config.config.endpoints", ["return_zip", "return_text", "return_json"]):
        yield


def test_unknown_path_get(
    mock_random_name, mock_endpoint_mapping, mock_valid_endpoints
):
    """Test GET request to /{path_name:path} endpoint."""
    # Mock the endpoint function being called
    with patch("myapp.router.random.choice") as mock_choice:
        mock_choice.return_value = "return_zip"  # Ensure 'return_zip' is selected

        response = client.get("/random_path")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Success"
    }  # Response from the mocked endpoint function
    mock_random_name.assert_called_once()  # Ensure random name generator is called
    mock_endpoint_mapping.assert_called_once()  # Ensure endpoint function is called


def test_unknown_path_post(
    mock_random_name, mock_endpoint_mapping, mock_valid_endpoints
):
    """Test POST request to /{path_name:path} endpoint."""
    # Mock the endpoint function being called
    with patch("myapp.router.random.choice") as mock_choice:
        mock_choice.return_value = "return_zip"  # Ensure 'return_zip' is selected

        response = client.post("/another_random_path")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Success"
    }  # Response from the mocked endpoint function
    mock_random_name.assert_called_once()  # Ensure random name generator is called
    mock_endpoint_mapping.assert_called_once()  # Ensure endpoint function is called


def test_unknown_path_put(mock_random_name):
    """Test PUT request to /{path_name:path} endpoint."""
    response = client.put("/some_random_path")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Resource 'random_file.txt' has been updated successfully."
    }
    mock_random_name.assert_called_once()  # Ensure random name generator is called


def test_unknown_path_delete(mock_random_name):
    """Test DELETE request to /{path_name:path} endpoint."""
    response = client.delete("/some_random_path")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Resource 'random_file.txt' has been deleted successfully."
    }
    mock_random_name.assert_called_once()  # Ensure random name generator is called


def test_unknown_path_invalid_endpoint(mock_random_name, mock_valid_endpoints):
    """Test case where the selected endpoint function is not callable."""
    with patch("myapp.router.endpoint_mapping.get") as mock_get:
        mock_get.return_value = None  # Simulate that no callable function is found

        response = client.get("/invalid_path")

    assert response.status_code == 500
    assert response.json() == {"detail": "Endpoint function is not callable."}
    mock_random_name.assert_called_once()  # Ensure random name generator is called


def test_unknown_path_exception_handling(mock_random_name):
    """Test case where an exception is raised while calling an endpoint function."""
    with patch("myapp.router.endpoint_mapping.get") as mock_get:
        mock_get.side_effect = Exception("Test error")  # Simulate an exception

        response = client.get("/random_path")

    assert response.status_code == 500
    assert response.json() == {"detail": "Test error"}
    mock_random_name.assert_called_once()  # Ensure random name generator is called
