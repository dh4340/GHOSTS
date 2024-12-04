import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("method", ["get"])
def test_return_zip_default(method):
    response = getattr(client, method)("/zip")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["get"])
def test_return_zip_filename(method, mock_file_name):
    response = getattr(client, method)(f"/zip/{mock_file_name}")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["get"])
def test_return_tar(method):
    response = getattr(client, method)("/tar")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["get"])
def test_return_tar_filename(method, mock_file_name):
    response = getattr(client, method)(f"/tar/{mock_tar_file_name}")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["post"])
def test_post_return_zip_default(method):
    response = getattr(client, method)("/zip")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["post"])
def test_post_return_zip_filename(method, mock_file_name):
    response = getattr(client, method)(f"/zip/{mock_file_name}")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["post"])
def test_post_return_tar_default(method):
    response = getattr(client, method)("/tar")
    assert response.status_code == 200

@pytest.mark.parametrize("method", ["post"])
def test_post_return_tar_filename(method, mock_file_name):
    response = getattr(client, method)(f"/tar/{mock_tar_file_name}")
    assert response.status_code == 200
