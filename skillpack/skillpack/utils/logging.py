"""Logging utilities for consistent output across skills."""

import logging
import sys
from typing import Optional


def setup_logging(
    name: str = "skillpack",
    level: int = logging.INFO,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """Set up and return a configured logger.

    Args:
        name: Logger name.
        level: Logging level (default: INFO).
        format_string: Custom format string (optional).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    # Create formatter
    if format_string is None:
        format_string = "%(levelname)s: %(message)s"

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_logger(name: str = "skillpack") -> logging.Logger:
    """Get an existing logger or create a new one.

    Args:
        name: Logger name.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
