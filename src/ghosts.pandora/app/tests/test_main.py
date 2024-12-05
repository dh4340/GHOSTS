import pytest


def test_about_endpoint(client):
    """Test the /about endpoint."""
    response = client.get("/about")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "0.6.0"
    assert data["message"] == "GHOSTS PANDORA server"
    assert "copyright" in data


@pytest.mark.parametrize(
    "path, expected_status, expected_content_type",
    [
        ("/file.txt", 200, "text/plain"),
        ("/file.pdf", 200, "application/pdf"),
        (
            "/file.doc",
            200,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
        ("/file.jpeg", 200, "image/JPEG"),
        ("/file.mp3", 200, "audio/wav"),
        ("/file.zip", 200, "application/zip"),
    ],
)
def test_file_type_handler(client, path, expected_status, expected_content_type):
    """Test dynamic file type handling."""
    response = client.get(path)

    assert response.status_code == expected_status

    if expected_status == 200:
        assert "Content-Type" in response.headers
        assert response.headers["Content-Type"].startswith(expected_content_type)


def test_file_type_handler_invalid(client):
    """Test file type handler for an unsupported file type."""
    response = client.get("/file.unsupported")
    assert response.status_code == 404
    assert response.json() == {"detail": "File type not supported."}


def test_file_type_handler_error(client, mocker):
    """Test file type handler when an exception is raised."""
    mock_return_pdf = mocker.patch(
        "routes.pdf_routes.return_pdf", side_effect=Exception("Mocked error")
    )
    response = client.get("/file.pdf")

    assert response.status_code == 500
    assert response.json() == {"detail": "Mocked error"}
    mock_return_pdf.assert_called_once()


def test_file_type_handler_no_extension(client):
    """Test file type handler with a path that has no extension."""
    response = client.get("/file_without_extension")
    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"].startswith("text/plain")


def test_proxy_unset():
    """Test that proxy environment variables are unset."""
    import os

    assert "http_proxy" not in os.environ
    assert "https_proxy" not in os.environ
    assert "HTTP_PROXY" not in os.environ
    assert "HTTPS_PROXY" not in os.environ
