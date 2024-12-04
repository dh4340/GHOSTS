def test_log_config(app_config):
    """
    Test logging configuration values.
    """
    assert app_config.LOG_DIR == "logs"
    assert app_config.LOG_FILE == "app.log"
    assert app_config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    assert isinstance(app_config.FILE_LOGGING, bool)
    assert "%(asctime)s" in app_config.LOG_JSON_FORMATTING


def test_ai_config(app_config):
    """
    Test AI-related configuration values.
    """
    assert isinstance(app_config.OLLAMA_ENABLED, bool)
    assert app_config.OLLAMA_API_URL.startswith("http")
    assert isinstance(app_config.OLLAMA_TIMEOUT, int)
    assert app_config.OLLAMA_TIMEOUT > 0

    # Validate models
    models = [
        app_config.HTML_MODEL,
        app_config.IMAGE_MODEL,
        app_config.JSON_MODEL,
        app_config.PPT_MODEL,
        app_config.SCRIPT_MODEL,
        app_config.STYLESHEET_MODEL,
        app_config.TEXT_MODEL,
        app_config.VOICE_MODEL,
        app_config.XLSX_MODEL,
        app_config.PDF_MODEL,
        app_config.CSV_MODEL,
    ]
    for model in models:
        assert isinstance(model, str)
        assert "llama" in model.lower()


def test_voice_config(app_config):
    """
    Test voice-related configuration values.
    """
    assert isinstance(app_config.VOICE_GENERATION_ENABLED, bool)


def test_image_config(app_config):
    """
    Test image-related configuration values.
    """
    assert isinstance(app_config.IMAGE_GENERATION_MODEL, str)
    assert "stabilityai" in app_config.IMAGE_GENERATION_MODEL
    assert isinstance(app_config.DIFFUSERS_LOCAL_FILES_ONLY, bool)


def test_video_config(app_config):
    """
    Test video-related configuration values.
    """
    assert isinstance(app_config.VIDEO_GENERATION_ENABLED, bool)


def test_faker_config(app_config):
    """
    Test Faker-related configuration values.
    """
    assert isinstance(app_config.FAKER_LOCALE, list)
    assert all(isinstance(locale, str) for locale in app_config.FAKER_LOCALE)


def test_endpoints(app_config):
    """
    Test endpoint list configuration values.
    """
    assert isinstance(app_config.endpoints, list)
    assert len(app_config.endpoints) > 0
    for endpoint in app_config.endpoints:
        assert isinstance(endpoint, str)
        assert endpoint.startswith("return_") or endpoint == "unknown_path"


def test_allowed_extensions(app_config):
    """
    Test allowed extensions configuration values.
    """
    assert isinstance(app_config.allowed_extensions, list)
    assert len(app_config.allowed_extensions) > 0
    for ext in app_config.allowed_extensions:
        assert isinstance(ext, str)
        assert ext.startswith(".")


def test_openapi_metadata(app_config):
    """
    Test OpenAPI metadata values.
    """
    metadata = app_config.OPENAPI_METADATA
    assert isinstance(metadata, dict)
    assert "title" in metadata
    assert "description" in metadata
    assert "version" in metadata
    assert "contact" in metadata
    assert "license_info" in metadata
    assert isinstance(metadata["openapi_tags"], list)
    assert len(metadata["openapi_tags"]) > 0

    for tag in metadata["openapi_tags"]:
        assert "name" in tag
        assert "description" in tag
