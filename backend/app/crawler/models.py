from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field

class PageType(str, Enum):
    HOMEPAGE = "HOMEPAGE"
    COLLECTION = "COLLECTION"
    PRODUCT = "PRODUCT"
    CART = "CART"

class PageResult(BaseModel):
    """
    Result of a single crawled page.
    """
    url: str = Field(..., description="The URL crawled.")
    page_type: PageType = Field(..., description="The type of page crawled.")
    status: str = Field(..., description="HTTP status or outcome (e.g., 'success', 'blocked', 'timeout').")
    html: Optional[str] = Field(None, description="The raw HTML content.")
    screenshot_path: Optional[str] = Field(None, description="Path to the saved screenshot.")
    response_time_ms: float = Field(..., description="Time taken to crawl the page in milliseconds.")
    error_reason: Optional[str] = Field(None, description="Detailed reason if the crawl failed.")

class StoreResult(BaseModel):
    """
    Complete result of crawling the entire store.
    """
    homepage: Optional[PageResult] = Field(None, description="Homepage crawl result.")
    collections: List[PageResult] = Field(default_factory=list, description="Collection crawl results.")
    products: List[PageResult] = Field(default_factory=list, description="Product crawl results.")
    cart: Optional[PageResult] = Field(None, description="Cart crawl result.")
