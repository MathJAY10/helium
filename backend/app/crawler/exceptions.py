class CrawlerError(Exception):
    """Base exception for crawler errors."""
    pass

class BotProtectionError(CrawlerError):
    """Raised when bot protection is detected (e.g. Cloudflare)."""
    pass

class MaxRetriesExceededError(CrawlerError):
    """Raised when maximum retries are exceeded for a transient failure."""
    pass

class InvalidUrlError(CrawlerError):
    """Raised when the URL is invalid or inaccessible."""
    pass

class CrawlerTimeoutError(CrawlerError):
    "Raised when a page fails to load within the timeout."
    pass

