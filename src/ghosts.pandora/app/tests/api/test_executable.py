import re
from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Mock values
mock_msi_content = b"This is a random MSI file with random content: "
mock_exe_content = b"This is a random EXE file with random content: "


def test_return_msi_with_random_filename(mock_paragraph):
    with patch("routes.executable_routes.generate_random_name") as mock_random_name:
        mock_random_name.return_value = "example_random_name.msi"

        response = client.get("/msi")
        assert response.status_code == 200

        content_disposition = response.headers.get("Content-Disposition", "")

        match = re.search(r'filename="?(.+\.msi)"?', content_disposition)
        assert match is not None, "Filename not found or does not end with .msi"

        filename = match.group(1)
        assert filename == "example_random_name.msi", f"Unexpected filename: {filename}"

        assert response.headers["Content-Type"] == "application/x-msdownload"

        assert b"This is a random MSI file with random content" in response.content


def test_return_msi_with_custom_filename(mock_paragraph):
    response = client.get("/msi/custom_filename")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_filename.msi"
    )
    assert response.headers["Content-Type"] == "application/x-msdownload"
    assert mock_msi_content in response.content


def test_return_exe_with_random_filename(mock_paragraph):
    with patch("routes.executable_routes.generate_random_name") as mock_random_name:
        mock_random_name.return_value = "travel_less.exe"

        response = client.get("/exe")
        assert response.status_code == 200

        content_disposition = response.headers.get("Content-Disposition", "")

        match = re.search(r'filename="?(.+\.exe)"?', content_disposition)
        assert match is not None, "Filename not found or does not end with .exe"
        filename = match.group(1)
        assert filename == "travel_less.exe", f"Unexpected filename: {filename}"

        assert response.headers["Content-Type"] == "application/octet-stream"
        assert b"This is a random EXE file with random content" in response.content


def test_return_exe_with_custom_filename(mock_paragraph):
    response = client.get("/exe/custom_filename")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=custom_filename.exe"
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert mock_exe_content in response.content


def test_return_msi_with_invalid_extension(mock_random_name):
    response = client.get("/msi/invalid_filename.txt")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=invalid_filename.txt.msi"
    )
    assert response.headers["Content-Type"] == "application/x-msdownload"


def test_return_exe_with_invalid_extension(mock_random_name):
    response = client.get("/exe/invalid_filename.txt")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=invalid_filename.txt.exe"
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
