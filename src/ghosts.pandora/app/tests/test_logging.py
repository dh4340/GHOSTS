import logging
import os
from unittest.mock import patch, MagicMock

import pytest
import app_logging





def test_setup_logger_creates_handlers(mock_config, tmp_path):
    """Test that setup_logger creates the appropriate handlers."""
    log_dir = tmp_path / "logs"
    os.makedirs(log_dir, exist_ok=True)

    with patch("your_module.LOG_DIR", log_dir), patch("your_module.LOG_FILE", "test.log"), patch(
        "your_module.LOG_JSON_FORMATTING", mock_config["LOG_JSON_FORMATTING"]
    ):
        logger = setup_logger("test_logger", level=logging.DEBUG)

    # Assert logger has two handlers: console and file
    assert len(logger.handlers) == 2
    assert any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers)
    assert any(isinstance(handler, logging.handlers.TimedRotatingFileHandler) for handler in logger.handlers)


def test_setup_logger_disables_file_logging(mock_config):
    """Test setup_logger with file logging disabled."""
    with patch("your_module.FILE_LOGGING", False):
        logger = setup_logger("test_logger_no_file", enable_file_logging=False)

    # Assert logger has only one handler: console
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_setup_logger_file_handler_error(mock_config, caplog):
    """Test setup_logger handles errors when adding a file handler."""
    with patch("your_module.TimedRotatingFileHandler", side_effect=OSError("Mocked file handler error")):
        logger = setup_logger("test_logger_file_error")

    # Ensure only one handler is added (console)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

    # Check that the error was logged
    assert "Failed to add file handler" in caplog.text


def test_configure_uvicorn_logging(mock_config, tmp_path):
    """Test that Uvicorn logging is configured properly."""
    log_dir = tmp_path / "logs"
    os.makedirs(log_dir, exist_ok=True)

    with patch("your_module.LOG_DIR", log_dir), patch("your_module.LOG_FILE", "uvicorn_test.log"), patch(
        "your_module.LOG_JSON_FORMATTING", mock_config["LOG_JSON_FORMATTING"]
    ):
        configure_uvicorn_logging()

    for uvicorn_logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uv_logger = logging.getLogger(uvicorn_logger_name)

        # Check that Uvicorn loggers have handlers
        assert len(uv_logger.handlers) > 0
        assert any(isinstance(handler, logging.StreamHandler) for handler in uv_logger.handlers)
        assert any(isinstance(handler, logging.handlers.TimedRotatingFileHandler) for handler in uv_logger.handlers)

        # Ensure log level is set correctly
        assert uv_logger.level == mock_config["LOG_LEVEL"]


def test_uvicorn_file_handler_error(mock_config, caplog):
    """Test that configure_uvicorn_logging handles errors when adding file handlers."""
    with patch("your_module.TimedRotatingFileHandler", side_effect=OSError("Mocked file handler error")):
        configure_uvicorn_logging()

    # Check that Uvicorn loggers have only console handlers
    for uvicorn_logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uv_logger = logging.getLogger(uvicorn_logger_name)
        assert len(uv_logger.handlers) == 1
        assert isinstance(uv_logger.handlers[0], logging.StreamHandler)

    # Ensure the error was logged
    assert "Failed to configure Uvicorn file handler" in caplog.text
