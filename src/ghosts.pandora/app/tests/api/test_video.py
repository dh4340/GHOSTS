from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


# def test_live_stream(mock_generate_frames):
#     """Test the /live_stream route."""
#     response = client.get("/live_stream")

#     assert response.status_code == 200
#     assert (
#         response.headers["content-type"] == "multipart/x-mixed-replace; boundary=frame"
#     )
#     # Validate that the mocked function was called
#     mock_generate_frames.assert_called_once()


# def test_video_with_generated_name(
#     mock_generate_video_with_cogvideox, mock_os_path_isfile
# ):
#     """Test the /video route when the file name is not provided (random generation)."""
#     with patch("utils.helper.generate_random_name", return_value="random_movie.mp4"):
#         response = client.get("/video")

#     assert response.status_code == 200
#     assert (
#         response.headers["Content-Disposition"]
#         == "attachment; filename=random_movie.mp4"
#     )
#     mock_generate_video_with_cogvideox.assert_called_once()  # Ensure video generation function was called
#     mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


# def test_video_with_requested_name(
#     mock_generate_video_with_cogvideox, mock_os_path_isfile
# ):
#     """Test the /video route when the file name is provided in the request."""
#     response = client.get("/video/some_movie.mp4")

#     assert response.status_code == 200
#     assert (
#         response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
#     )
#     mock_generate_video_with_cogvideox.assert_called_once_with(
#         prompt="some_movie",
#         output_filename="static/some_movie.mp4",
#         num_frames=49,
#         guidance_scale=6,
#         seed=42,
#     )
#     mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


# def test_video_generation_disabled(mock_video_generation_disabled, mock_os_path_isfile):
#     """Test the /video route when video generation is disabled."""
#     response = client.get("/video/some_movie.mp4")

#     assert response.status_code == 200
#     assert (
#         response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
#     )
#     mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called


# def test_fallback_video_when_not_found(
#     mock_generate_video_with_cogvideox, mock_os_path_isfile
# ):
#     """Test the /video route when the requested video file is not found, falling back to static content."""
#     with patch("os.path.isfile", side_effect=lambda x: x == "static/fallback.mp4"):
#         response = client.get("/video/nonexistent_video.mp4")

#     assert response.status_code == 200
#     assert (
#         response.headers["Content-Disposition"] == "attachment; filename=fallback.mp4"
#     )
#     mock_generate_video_with_cogvideox.assert_called_once()  # Ensure video generation function was called
#     mock_os_path_isfile.assert_called()  # Ensure file existence check was called


# def test_video_generation_failure(
#     mock_generate_video_with_cogvideox, mock_os_path_isfile
# ):
#     """Test the /video route when video generation fails and fallback is used."""
#     with patch(
#         "utils.text2video.generate_video_with_cogvideox",
#         side_effect=Exception("Video generation error"),
#     ):
#         response = client.get("/video/some_movie.mp4")

#     assert response.status_code == 200
#     assert (
#         response.headers["Content-Disposition"] == "attachment; filename=some_movie.mp4"
#     )
#     mock_os_path_isfile.assert_called_once()  # Ensure file existence check was called
