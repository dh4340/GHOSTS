from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


# def test_generate_synthesised_conversation(
#     mock_generate_document_with_ollama,
#     mock_generate_audio_response,
#     mock_create_temp_audio_file,
#     mock_voice_generation_enabled,
# ):
#     """Test the /call route with voice generation enabled."""
#     response = client.get("/call")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "audio/wav"
#     assert (
#         response.content == b"fake_audio_data"
#     )  # Check if the audio content is returned

#     mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
#     mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called
#     mock_create_temp_audio_file.assert_called_once()  # Ensure temp file creation was called


# def test_generate_synthesised_conversation_text(
#     mock_generate_document_with_ollama, mock_voice_generation_disabled
# ):
#     """Test the /call route with voice generation disabled."""
#     response = client.get("/call")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "text/plain"
#     assert (
#         response.text == "actor1: Hello!\nactor2: Hi there!"
#     )  # Check if the conversation script is returned as text

#     mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called


# def test_generate_synthesised_conversation_failure(mock_generate_document_with_ollama):
#     """Test the /call route when script generation fails."""
#     with patch("utils.ollama.generate_document_with_ollama", return_value=None):
#         response = client.get("/call")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "text/plain"
#     assert (
#         response.text == "Failed to generate conversation script."
#     )  # Check if failure message is returned

#     mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called


# def test_audio_generation_failure(
#     mock_generate_document_with_ollama, mock_generate_audio_response
# ):
#     """Test the /call route when audio generation fails."""
#     with patch("utils.voice.generate_audio_response", return_value=None):
#         response = client.get("/call")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "text/plain"
#     assert (
#         response.text == "Audio synthesis failed."
#     )  # Check if failure message is returned

#     mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
#     mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called


# def test_generate_synthesised_conversation_with_custom_actors(
#     mock_generate_document_with_ollama,
#     mock_generate_audio_response,
#     mock_create_temp_audio_file,
#     mock_voice_generation_enabled,
# ):
#     """Test the /call route with custom actors."""
#     response = client.get("/call?actor1=developer&actor2=manager")

#     assert response.status_code == 200
#     assert response.headers["Content-Type"] == "audio/wav"
#     assert (
#         response.content == b"fake_audio_data"
#     )  # Check if the audio content is returned

#     mock_generate_document_with_ollama.assert_called_once()  # Ensure script generation was called
#     mock_generate_audio_response.assert_called_once()  # Ensure audio generation was called
#     mock_create_temp_audio_file.assert_called_once()  # Ensure temp file creation was called
