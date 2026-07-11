import asyncio
from typing import Callable, Any, TypeVar, Coroutine
from functools import wraps
from app.utils.logger import get_logger
from app.llm.exceptions import LLMRetryExceededError

logger = get_logger()
T = TypeVar('T')

def retry_llm_call(max_retries: int = 3, initial_backoff: float = 2.0) -> Callable:
    """
    Retries an async function on specific exceptions (Timeout, 429, 500, 503)
    with exponential backoff.
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            backoff = initial_backoff
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)
                    # Check for retriable HTTP errors or timeouts
                    is_retriable = any(code in error_str for code in ["429", "500", "503", "504"]) or "timeout" in error_str.lower()
                    
                    if not is_retriable or attempt == max_retries:
                        if attempt == max_retries and is_retriable:
                            logger.error(f"LLM call failed after {max_retries} attempts. Last error: {e}")
                            raise LLMRetryExceededError(f"Max retries exceeded: {e}")
                        raise e # Reraise if not retriable
                    
                    logger.warning(f"LLM call failed with {e}. Retrying in {backoff} seconds... (Attempt {attempt}/{max_retries})")
                    await asyncio.sleep(backoff)
                    backoff *= 2
            
            raise LLMRetryExceededError("Max retries exceeded")
        return wrapper
    return decorator
