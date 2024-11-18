import pyttsx3
import tempfile
import os
import time
from app_logging import setup_logger
from typing import Optional

# Set up logging
logger = setup_logger(__name__)


def generate_audio_response(conversation_script: str) -> Optional[bytes]:
    """Generate audio from a conversation script using pyttsx3 with two different voices.

    Args:
        conversation_script (str): The text of the conversation to be synthesized.

    Returns:
        Optional[bytes]: The synthesized audio in a binary format, or None if synthesis fails.
    """
    try:
        # Initialize the pyttsx3 engine
        logger.debug("Initializing pyttsx3 engine.")
        engine = pyttsx3.init(driverName="espeak")

        # Get the available voices
        voices = engine.getProperty("voices")
        logger.debug("Available voices retrieved: %d", len(voices))

        # Set voices for actor1 and actor2
        actor1_voice_id = voices[0].id if len(voices) > 0 else None
        actor2_voice_id = voices[1].id if len(voices) > 1 else actor1_voice_id
        logger.debug("Actor1 voice ID: %s", actor1_voice_id)
        logger.debug("Actor2 voice ID: %s", actor2_voice_id)

        # Check if at least one voice is available
        if not actor1_voice_id:
            logger.error("No voices available for audio synthesis.")
            return None

        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_audio_file:
            temp_audio_path = temp_audio_file.name
        logger.debug("Temporary file created for audio: %s", temp_audio_path)

        # Loop through the conversation script and synthesize each line
        lines = conversation_script.strip().split("\n")
        logger.debug("Processing %d lines of dialogue for synthesis.", len(lines))

        for line in lines:
            dialogue = ""  # Initialize dialogue to ensure it's always defined
            if line.startswith("actor1:"):
                # Set actor1's voice and synthesize dialogue
                dialogue = line.replace("actor1:", "").strip()
                engine.setProperty("voice", actor1_voice_id)
                logger.debug("Actor1 dialogue: %s", dialogue)
            elif line.startswith("actor2:"):
                # Set actor2's voice and synthesize dialogue
                dialogue = line.replace("actor2:", "").strip()
                engine.setProperty("voice", actor2_voice_id)
                logger.debug("Actor2 dialogue: %s", dialogue)
            else:
                logger.warning("Unexpected line format: %s", line)
                continue

        # Synthesize the dialogue and save to the temporary file
        if dialogue:
            logger.debug("Saving dialogue to file: %s", dialogue)
            engine.save_to_file(dialogue, temp_audio_path)
            logger.debug("Running pyttsx3 engine to process queued audio commands.")
            engine.runAndWait()
            engine.stop()

        logger.debug("pyttsx3 engine finished processing.")

        # Read the audio data from the temporary file
        if os.path.exists(temp_audio_path):
            logger.debug("Reading audio data from temporary file.")
            with open(temp_audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
            logger.debug("Audio data read successfully, returning audio data.")
        else:
            logger.error("Temporary audio file not found: %s", temp_audio_path)
            return None

        # Clean up the temporary file
        os.remove(temp_audio_path)
        logger.debug("Temporary audio file deleted: %s", temp_audio_path)

        return audio_data

    except Exception as e:
        logger.error("Error during audio synthesis: %s", e, exc_info=True)
        return None
