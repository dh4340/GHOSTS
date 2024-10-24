# Gradio API Interface

This project provides a web-based user interface for interacting with the authentication and API services of the Ghosts Shadows application. It allows users to log in, sign up, and query the shadows API through a user-friendly Gradio interface.

## Features

- **User Authentication**: Users can log in or sign up to access the API.
- **API Querying**: Once authenticated, users can query the shadows API with specific models.
- **Dynamic Interface**: Built with Gradio, providing a responsive UI with tabs for easy navigation.

## Project Structure

```
ghost.shadows/
│
├── ui/
│   ├── __init__.py
│   ├── main.py          # Entry point for the Gradio app
│   ├── auth.py          # Handles authentication logic
│   ├── api.py           # Contains API interaction logic
│   ├── interface.py      # Defines the Gradio UI components
│   └── config.py        # Configuration settings (e.g., URLs)
```

## Requirements

- Python 3.10+
- Gradio
- Requests

You can install the required packages using pip:

```bash
pip install gradio requests
```

## Environment Variables

The application uses the following environment variables to configure the authentication and shadows service URLs:

- `AUTH_URL`: The base URL for the authentication service (default: `http://0.0.0.0:8000`)
- `SHADOWS_URL`: The base URL for the shadows API service (default: `http://0.0.0.0:5900`)

You can set these variables in your terminal before running the application:

```bash
export AUTH_URL="http://your_auth_service_url"
export SHADOWS_URL="http://your_shadows_api_url"
```

## Running the Application

To start the Gradio UI, run the following command in your terminal:

```bash
python -m ghost.shadows.ui.main
```

The application will be accessible at `http://0.0.0.0:7860`.

## Usage

1. **Authenticate**:
   - Navigate to the "Authenticate" tab.
   - Enter your username and password.
   - Choose whether you are a new or existing user and click "Submit".

2. **Query the API**:
   - Once logged in, navigate to the "Query API" tab.
   - Enter your query and select the desired model.
   - Click "Submit" to get the response from the API.

## Troubleshooting

- Ensure the authentication and shadows services are running and accessible.
- Check for any errors in the terminal where you run the Gradio app for debugging information.

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
