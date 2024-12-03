import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def default_iso_filename():
    """Fixture to mock default ISO filename."""
    return "random_file.iso"


@pytest.fixture
def custom_iso_filename():
    """Fixture to mock custom ISO filename."""
    return "test_file.iso"


@pytest.fixture
def missing_extension_filename():
    """Fixture to mock ISO filename without extension."""
    return "test_file"


def test_return_iso_default_name(default_iso_filename):
    """Test ISO generation with default file name."""
    response = client.get("/iso")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith(
        f"attachment; filename={default_iso_filename}"
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.content.startswith(b"This is a random ISO file")


def test_return_iso_custom_name(custom_iso_filename):
    """Test ISO generation with a custom file name."""
    response = client.get(f"/iso/{custom_iso_filename}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == f"attachment; filename={custom_iso_filename}"
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.content.startswith(b"This is a random ISO file")


def test_return_iso_missing_extension(missing_extension_filename):
    """Test ISO generation with a missing .iso extension."""
    response = client.get(f"/iso/{missing_extension_filename}")
    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == f"attachment; filename={missing_extension_filename}.iso"
    )
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.content.startswith(b"This is a random ISO file")
