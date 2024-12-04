import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_generate_frames():
    """Fixture to mock the generate_frames function used in live_stream."""
    with patch("utils.helper.generate_frames") as mock_func:
        mock_func.return_value = iter(
            [b"frame1", b"frame2", b"frame3"]
        )  # Mocking frame generation
        yield mock_func


@pytest.fixture
def mock_generate_video_with_cogvideox():
    """Fixture to mock the video generation function."""
    with patch("utils.text2video.generate_video_with_cogvideox") as mock_func:
        mock_func.return_value = (
            "generated_video.mp4"  # Mock successful video generation
        )
        yield mock_func


@pytest.fixture
def mock_os_path_isfile():
    """Fixture to mock os.path.isfile to simulate video file existence."""
    with patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = True  # Simulate that the video file exists
        yield mock_isfile


@pytest.fixture
def mock_video_generation_disabled():
    """Fixture to simulate that video generation is disabled."""
    with patch("config.config.VIDEO_GENERATION_ENABLED", False):
        yield


def test_live_stream(mock_generate_frames):
    """Test the /live_stream route."""
    response = client.get("/live_stream")

    assert response.status_code == 200
    assert (
        response.headers["content-type"] == "multipart/x-mixed-replace; boundary=frame"
    )
    mock_generate_frames.assert_called_once()  # Ensure generate_frames was called


def test_video_with_generated_name(
    mock_generate_video_with_cogvideox, mock_os_path_isfile
):
    """Test the /video route when the file name is not provided (random generation)."""
    with patch("utils.helper.generate_random_name", return_value="random_movie.mp4"):
        response = client.get("/video")

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"]
        == "attachment; filename=random_movie.mp4"
    )
    mock_generate_video_with_cogvideox.assert_called_once()  # Ensure video generation function was called
    mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


def test_video_with_requested_name(
    mock_generate_video_with_cogvideox, mock_os_path_isfile
):
    """Test the /video route when the file name is provided in the request."""
    response = client.get("/video/some_movie.mp4")

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
    )
    mock_generate_video_with_cogvideox.assert_called_once_with(
        prompt="some_movie",
        output_filename="static/some_movie.mp4",
        num_frames=49,
        guidance_scale=6,
        seed=42,
    )
    mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


def test_video_generation_disabled(mock_video_generation_disabled, mock_os_path_isfile):
    """Test the /video route when video generation is disabled."""
    response = client.get("/video/some_movie.mp4")

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
    )
    mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


def test_fallback_video_when_not_found(
    mock_generate_video_with_cogvideox, mock_os_path_isfile
):
    """Test the /video route when the requested video file is not found, falling back to static content."""
    with patch("os.path.isfile", side_effect=lambda x: x == "static/fallback.mp4"):
        response = client.get("/video/nonexistent_video.mp4")

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=fallback.mp4"
    )
    mock_generate_video_with_cogvideox.assert_called_once()  # Ensure video generation function was called
    mock_os_path_isfile.assert_called()  # Ensure file existence check was called


def test_video_generation_failure(
    mock_generate_video_with_cogvideox, mock_os_path_isfile
):
    """Test the /video route when video generation fails and fallback is used."""
    with patch(
        "utils.text2video.generate_video_with_cogvideox",
        side_effect=Exception("Video generation error"),
    ):
        response = client.get("/video/some_movie.mp4")

    assert response.status_code == 200
    assert (
        response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
    )
    mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called
