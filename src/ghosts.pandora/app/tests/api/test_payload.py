from unittest.mock import MagicMock, mock_open, patch

import pytest
from app import main
from app.routes.payload_routes import router
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create a test FastAPI app and include the router
app = FastAPI()
app.include_router(router)
client = TestClient(main)


@patch("app.routes.payload_routes.get_config")
@patch("app.routes.payload_routes.get_payload_path")
@patch("builtins.open", new_callable=mock_open, read_data=b'{"key": "value"}')
def test_payload_match(
    mock_open_file, mock_get_payload_path, mock_get_config, mock_config, mock_base_dir
):
    """Test that the payload matches the expected response."""
    mock_get_config.return_value = mock_config
    mock_get_payload_path.side_effect = (
        lambda base_dir, filename: f"{mock_base_dir}/{filename}"
    )

    response = client.get("/payloads/api/example")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Disposition"] == "inline; filename=example1.json"
    assert response.content == b'{"key": "value"}'


@patch("app.routes.payload_routes.get_config")
def test_payload_no_match(mock_get_config, mock_config):
    """Test that the endpoint returns 404 for an unknown path."""
    mock_get_config.return_value = mock_config

    response = client.get("/payloads/unknown/path")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payload not found."


@patch("app.routes.payload_routes.get_config")
@patch("app.routes.payload_routes.get_payload_path")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_missing_file(
    mock_open_file, mock_get_payload_path, mock_get_config, mock_config, mock_base_dir
):
    """Test that the endpoint returns 404 for a missing file."""
    mock_get_config.return_value = mock_config
    mock_get_payload_path.side_effect = (
        lambda base_dir, filename: f"{mock_base_dir}/{filename}"
    )

    response = client.get("/payloads/api/missing")
    assert response.status_code == 404
    assert "File missing_file.json not found." in response.json()["detail"]


@patch("app.routes.payload_routes.get_config")
def test_invalid_config_format(mock_get_config):
    """Test for invalid configuration during startup."""
    # Simulate a config missing the required "payloads" section
    invalid_config = MagicMock()
    invalid_config.__contains__.return_value = False  # Simulates missing section
    mock_get_config.return_value = invalid_config

    response = client.get("/payloads/api/invalid_config")
    assert response.status_code == 500
    assert response.json()["detail"] == "Configuration error."


@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/payloads/api/example", 200),
        ("/payloads/unknown/path", 404),
        ("/payloads/api/missing", 404),
    ],
)
@patch("app.routes.payload_routes.get_config")
@patch("app.routes.payload_routes.get_payload_path")
@patch("builtins.open", new_callable=mock_open, read_data=b"{}")
def test_parametrized_payloads(
    mock_open_file,
    mock_get_payload_path,
    mock_get_config,
    mock_config,
    path,
    expected_status,
    mock_base_dir,
):
    """Test multiple payload scenarios."""
    mock_get_config.return_value = mock_config
    mock_get_payload_path.side_effect = (
        lambda base_dir, filename: f"{mock_base_dir}/{filename}"
    )

    response = client.get(path)
    assert response.status_code == expected_status
