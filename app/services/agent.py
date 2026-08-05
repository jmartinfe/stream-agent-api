import os
from pathlib import Path
from typing import AsyncGenerator, Dict, List
from openai import OpenAI
from app.core.exceptions import MissingAPIKeyError, MissingPromptFileError, ResponseGenerationError, SessionNotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)
PROMPT_FILE = Path("data/system_prompt.txt")
SESSIONS: Dict[str, List[dict]] = {}

def get_system_prompt() -> str:
    if not PROMPT_FILE.exists():
        logger.error("Missing system prompt file: %s", PROMPT_FILE)
        raise MissingPromptFileError()
    return PROMPT_FILE.read_text(encoding="utf-8")

# Initialize the OpenAI client using the API key from environment variables
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MissingAPIKeyError()
    return OpenAI(api_key=api_key)

def get_or_create_session(session_id: str) -> List[dict]:
    """ 
    Retrieve the session history for a given session_id, or create a new one if it doesn't exist.
    """
    if session_id not in SESSIONS:
        logger.info("Creating new session history for session_id=%s", session_id)
        SESSIONS[session_id] = []
    return SESSIONS[session_id]

def clear_session(session_id: str) -> None:
    """ 
    Clear the session history for a given session_id.
    """
    if session_id not in SESSIONS:
        raise SessionNotFoundError(f"Session {session_id} not found.")
    del SESSIONS[session_id]

def clear_all_sessions() -> None:
    """ 
    Clear all session histories.
    """
    SESSIONS.clear()

async def response_generator(session_id: str, user_message: str) -> AsyncGenerator[str, None]:
    """
    Asynchronous generator that streams responses from the OpenAI API based on user input.
    Args:
        session_id (str): Unique identifier for the chat session.
        user_message (str): The message from the user to which the assistant should respond.
        Yields:
        str: Chunks of the assistant's response as they are generated.
    """
    logger.info("Generating chat response for session_id=%s", session_id)
    client = get_openai_client()
    system_prompt = get_system_prompt()
    session_history = get_or_create_session(session_id)

    # Record the user's message in the session history
    session_history.append({"role": "user", "content": user_message})

    # Prepare the messages for the OpenAI API, starting with the system prompt and including the session history
    formatted_messages = [{"role": "system", "content": system_prompt}]
    formatted_messages.extend(session_history)

    # Stream the response from the OpenAI API
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=formatted_messages,
            max_tokens=400,
            temperature=0.7,
            stream=True,
        )
    except Exception as e:
        logger.exception("Failed to start OpenAI stream for session_id=%s", session_id)
        raise ResponseGenerationError(f"Failed to start response stream: {e}")

    full_response = ""

    try:
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
    except Exception as e:
        logger.exception("Error while streaming OpenAI response for session_id=%s", session_id)
        raise ResponseGenerationError(f"Error during response stream: {e}")

    # After streaming is complete, record the assistant's full response in the session history
    session_history.append({"role": "assistant", "content": full_response})
    logger.info("Completed chat response for session_id=%s", session_id)
