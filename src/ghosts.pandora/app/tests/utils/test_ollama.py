import pytest
from utils.ollama import generate_document_with_ollama
from requests.exceptions import Timeout, RequestException


# def test_generate_document_with_ollama_success(mocker, example_prompt, example_model, mock_ollama_url, mock_ollama_timeout):
#     """Test successful document generation using pytest-mock."""
#     # Mock the requests.post response
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"response": "This is a generated document."}
#     mock_post = mocker.patch("utils.ollama.requests.post", return_value=mock_response)

#     # Run the function
#     result = generate_document_with_ollama(
#         example_prompt, example_model, timeout=mock_ollama_timeout
#     )

#     # Assertions
#     mock_post.assert_called_once_with(
#         mock_ollama_url,
#         json={"model": example_model, "prompt": example_prompt, "stream": False},
#         timeout=mock_ollama_timeout,
#     )
#     assert result == "This is a generated document"


# def test_generate_document_with_ollama_timeout(mocker, example_prompt, example_model, mock_ollama_url, mock_ollama_timeout):
#     """Test timeout handling."""
#     # Mock the requests.post to raise a timeout
#     mocker.patch("utils.ollama.requests.post", side_effect=Timeout)

#     # Run the function and assert the exception
#     with pytest.raises(Timeout):
#         generate_document_with_ollama(example_prompt, example_model, timeout=mock_ollama_timeout)



def test_generate_document_with_ollama_non_200_response(
    mocker, example_prompt, example_model, mock_ollama_url, mock_ollama_timeout
):
    """Test handling of non-200 responses."""
    # Mock the requests.post response with a non-200 status code
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mocker.patch("utils.ollama.requests.post", return_value=mock_response)

    # Run the function
    result = generate_document_with_ollama(
        example_prompt, example_model, timeout=mock_ollama_timeout
    )

    # Assertions
    assert result is None


# def test_generate_document_with_ollama_request_exception(mocker, example_prompt, example_model, mock_ollama_url, mock_ollama_timeout):
#     """Test handling of generic request exceptions."""
#     # Mock the requests.post to raise a generic request exception
#     mocker.patch(
#         "utils.ollama.requests.post",
#         side_effect=RequestException("Network error"),
#     )

#     # Run the function and assert the exception
#     with pytest.raises(RequestException):
#         generate_document_with_ollama(example_prompt, example_model, timeout=mock_ollama_timeout)
