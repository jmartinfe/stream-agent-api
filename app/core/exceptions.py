from typing import Optional


class AppError(Exception):
    """Base exception for application-specific errors."""

    status_code = 500
    default_detail = "An application error occurred."

    def __init__(self, detail: Optional[str] = None):
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class ConfigurationError(AppError):
    """Errors related to application configuration."""

    status_code = 500


class MissingAPIKeyError(ConfigurationError):
    default_detail = "OPENAI_API_KEY environment variable is missing."


class MissingPromptFileError(ConfigurationError):
    default_detail = "System prompt file is missing."


class SessionError(AppError):
    """Errors related to session management."""

    status_code = 404


class SessionNotFoundError(SessionError):
    default_detail = "The specified session ID was not found."


class ResponseGenerationError(AppError):
    """Errors raised while generating a response from the AI service."""

    status_code = 502
