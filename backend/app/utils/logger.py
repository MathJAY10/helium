import logging
import sys
from functools import lru_cache

class StructuredLogger:
    """
    Wrapper around standard logging to enforce structured logging patterns.
    Supports injecting metrics like request_id and durations later.
    """
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Avoid duplicate handlers if already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, msg: str, **kwargs):
        self._log(logging.INFO, msg, **kwargs)

    def error(self, msg: str, **kwargs):
        self._log(logging.ERROR, msg, **kwargs)
        
    def warning(self, msg: str, **kwargs):
        self._log(logging.WARNING, msg, **kwargs)

    def exception(self, msg: str, **kwargs):
        if kwargs:
            extra_info = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            msg = f"{msg} | {extra_info}"
        self.logger.exception(msg)

    def debug(self, msg: str, **kwargs):
        self._log(logging.DEBUG, msg, **kwargs)

    def _log(self, level: int, msg: str, **kwargs):
        # Format kwargs into the message for structured-like output
        if kwargs:
            extra_info = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            msg = f"{msg} | {extra_info}"
        self.logger.log(level, msg)

@lru_cache()
def get_logger() -> StructuredLogger:
    """
    Dependency provider for Logger.
    """
    from app.utils.config import get_settings
    settings = get_settings()
    return StructuredLogger("CRO_Engine", settings.LOG_LEVEL)
