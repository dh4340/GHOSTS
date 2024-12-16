from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_return_iso_with_random_filename():
    """Test ISO generation with a random file name."""
    with patch("routes.iso_routes.generate_random_name") as mock_random_name:
        mock_random_name.return_value = "random_name.iso"

        response = client.get("/iso")
        assert response.status_code == 200

        content_disposition = response.headers.get("Content-Disposition", "")
        print(f"Content-Disposition header: {content_disposition}")  # Debugging

        assert content_disposition.startswith(
            'attachment; filename="random_name.iso"'
        ), f"Unexpected Content-Disposition header: {content_disposition}"

        assert response.headers["Content-Type"] == "application/octet-stream"

        assert response.content.startswith(b"This is a random ISO file")


def test_return_iso_custom_name(custom_iso_filename):
    """Test ISO generation with a custom file name."""
    response = client.get(f"/iso/{custom_iso_filename}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == f'attachment; filename="{custom_iso_filename}"'
    ), f"Unexpected Content-Disposition header: {response.headers['Content-Disposition']}"
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.content.startswith(b"This is a random ISO file")


def test_return_iso_missing_extension(missing_extension_filename):
    """Test ISO generation with a missing .iso extension."""
    response = client.get(f"/iso/{missing_extension_filename}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == f'attachment; filename="{missing_extension_filename}.iso"'
    ), f"Unexpected Content-Disposition header: {response.headers['Content-Disposition']}"
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.content.startswith(b"This is a random ISO file")
