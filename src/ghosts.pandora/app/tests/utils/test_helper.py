import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
import random
import numpy as np
from app_logging import setup_logger
from utils.helper import (
    generate_random_name,
    generate_frames,
    generate_zip_stream,
    generate_video_from_frames,
    generate_image_response,
    create_random_files,
    generate_archive,
    create_response,
    clean_content,
)
from PIL import Image


# Mock logger
logger = setup_logger(__name__)


@pytest.mark.parametrize("extension", ["", ".txt", ".jpg", ".json"])
def test_generate_random_name(extension):
    name = generate_random_name(extension)
    assert name.endswith(extension)
    assert len(name) > len(extension)


def test_generate_frames():
    frame_gen = generate_frames()
    frame = next(frame_gen)
    assert b"--frame\r\n" in frame
    assert b"Content-Type: image/jpeg\r\n\r\n" in frame


# def test_generate_zip_stream():
#     with patch("zipstream.ZipFile") as mock_zip:
#         mock_zip.return_value = MagicMock()
#         mock_zip.return_value.__iter__.return_value = [b"chunk1", b"chunk2"]
#         result = list(generate_zip_stream(mock_zip))
#         assert result == [b"chunk1", b"chunk2"]


def test_generate_video_from_frames(tmp_path):
    output_file = tmp_path / "test_video.mp4"
    generate_video_from_frames(str(output_file), frame_count=10, fps=5)
    assert output_file.exists()


@pytest.mark.parametrize("request_type", ["jpg", "png"])
def test_generate_image_response(request_type):
    response = generate_image_response(request_type)
    assert response.status_code == 200
    assert f"image/{request_type}" in response.media_type
    assert "attachment; filename=" in response.headers["Content-Disposition"]


def test_create_random_files():
    num_files = 5
    files = create_random_files(num_files)
    assert len(files) == num_files
    for name, content in files:
        assert isinstance(name, str)
        assert isinstance(content, bytes)


# @pytest.mark.parametrize("archive_type", ["zip", "tar"])
# def test_generate_archive(archive_type):
#     archive_name = f"test_archive.{archive_type}"
#     buffer = generate_archive(archive_name, archive_type)
#     assert isinstance(buffer, BytesIO)

#     size = buffer.getbuffer().nbytes
#     logger.debug(f"Generated archive size: {size} bytes")

#     assert size > 0  # Ensure the buffer is not empty


def test_create_response():
    buffer = BytesIO(b"test content")
    file_name = "test_file.txt"
    response = create_response(buffer, file_name, "text/plain")
    assert response.media_type == "text/plain"
    assert (
        f"attachment; filename={file_name}" in response.headers["Content-Disposition"]
    )


@pytest.mark.parametrize(
    "content, expected",
    [
        ("```html<html></html>```", "<html></html>"),
        ("```html<html>Test</html>```", "<html>Test</html>"),
        ("<html>Content</html>", "<html>Content</html>"),
    ],
)
def test_clean_content(content, expected):
    assert clean_content(content) == expected
