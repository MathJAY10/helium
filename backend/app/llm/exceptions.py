class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass

class LLMValidationError(LLMError):
    """Raised when the LLM output fails schema validation."""
    pass

class LLMRetryExceededError(LLMError):
    """Raised when the maximum number of retries for an LLM call is exceeded."""
    pass
