import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


DEFAULT_LOG_LEVEL = logging.INFO


def init_logging(level: int = DEFAULT_LOG_LEVEL, log_file: Optional[str] = None) -> None:
    """Initialize application logging.

    Args:
        level: logging level (e.g. logging.INFO)
        log_file: optional path to a file to write logs to. If not provided,
            logs will be written to ./logs/app.log relative to project root.
    """
    # Determine log file path
    if log_file is None:
        project_root = Path(__file__).resolve().parents[3]
        logs_dir = project_root / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = str(logs_dir / "app.log")

    # Root logger
    root = logging.getLogger()
    root.setLevel(level)
    if root.handlers:
        root.handlers.clear()

    # Formatter
    fmt = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # Rotating file handler
    fh = logging.handlers.RotatingFileHandler(
        filename=log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(level)
    fh.setFormatter(fmt)
    root.addHandler(fh)


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a module.

    Call init_logging() once at application startup.
    """
    return logging.getLogger(name)


__all__ = ["init_logging", "get_logger"]
