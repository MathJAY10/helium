import time
from typing import Optional, Dict, Tuple
from app.utils.config import get_settings
from app.crawler.models import PageResult

class CrawlerCache:
    """
    In-memory TTL cache for crawler results, keyed by URL.
    """
    def __init__(self):
        # Dict[url, Tuple[timestamp, PageResult]]
        self._cache: Dict[str, Tuple[float, PageResult]] = {}
        settings = get_settings()
        self.ttl = settings.CACHE_TTL

    def get(self, url: str) -> Optional[PageResult]:
        """
        Retrieve a cached PageResult if it exists and has not expired.
        """
        if url in self._cache:
            timestamp, result = self._cache[url]
            if time.time() - timestamp <= self.ttl:
                return result
            else:
                del self._cache[url]
        return None

    def set(self, url: str, result: PageResult) -> None:
        """
        Store a PageResult in the cache.
        """
        self._cache[url] = (time.time(), result)

    def clear(self):
        """Clear the entire cache."""
        self._cache.clear()

# Global cache instance
crawler_cache = CrawlerCache()
