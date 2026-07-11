from pydantic import BaseModel, Field

class APIError(BaseModel):
    """
    Base API Error response model.
    """
    error: str = Field(..., description="The type of error.")
    detail: str = Field(..., description="Detailed error message.")

class InvalidURLError(APIError):
    """
    Returned when the provided URL is not a valid Shopify store or is unreachable.
    """
    error: str = "Invalid URL"

class TimeoutError(APIError):
    """
    Returned when crawling or LLM generation takes too long.
    """
    error: str = "Timeout"

class CrawlerFailureError(APIError):
    """
    Returned when Playwright fails to extract the required DOM elements or gets blocked.
    """
    error: str = "Crawler Failure"

class GeminiFailureError(APIError):
    """
    Returned when the Gemini API is unreachable, fails to parse the prompt, or returns invalid JSON.
    """
    error: str = "Gemini Failure"

class ValidationError(APIError):
    """
    Returned when the extracted evidence or LLM output fails Pydantic validation.
    """
    error: str = "Validation Error"
