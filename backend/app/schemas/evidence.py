from enum import Enum
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class ExtractionStatus(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    INSUFFICIENT = "INSUFFICIENT"

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class FieldEvidence(BaseModel, Generic[T]):
    """
    Wraps an extracted value with its extraction status and confidence.
    """
    value: Optional[T] = Field(None, description="The extracted value.")
    status: ExtractionStatus = Field(..., description="Status of the extraction.")
    confidence: ConfidenceLevel = Field(..., description="Parser confidence in the extracted value.")

class HomepageEvidence(BaseModel):
    """Evidence extracted from the Shopify homepage."""
    url: str
    hero_heading: FieldEvidence[str]
    hero_cta: FieldEvidence[str]
    announcement_bar: FieldEvidence[str]
    navigation_links: FieldEvidence[List[str]]
    featured_collections: FieldEvidence[List[str]]
    newsletter_present: FieldEvidence[bool]
    trust_badges: FieldEvidence[List[str]]
    social_links: FieldEvidence[List[str]]

class CollectionEvidence(BaseModel):
    """Evidence extracted from a single Shopify collection page."""
    url: str
    collection_title: FieldEvidence[str]
    filters_present: FieldEvidence[bool]
    sorting_present: FieldEvidence[bool]
    product_count: FieldEvidence[int]
    sale_badges: FieldEvidence[List[str]]
    pagination_present: FieldEvidence[bool]

class ProductEvidence(BaseModel):
    """Evidence extracted from a single Shopify Product Detail Page (PDP)."""
    url: str
    product_title: FieldEvidence[str]
    brand: FieldEvidence[str]
    price: FieldEvidence[str]
    compare_at_price: FieldEvidence[str]
    discount_percentage: FieldEvidence[str]
    currency: FieldEvidence[str]
    rating: FieldEvidence[str]
    review_count: FieldEvidence[int]
    image_count: FieldEvidence[int]
    video_present: FieldEvidence[bool]
    sticky_add_to_cart: FieldEvidence[bool]
    variants_present: FieldEvidence[bool]
    size_guide_present: FieldEvidence[bool]
    shipping_text: FieldEvidence[str]
    returns_text: FieldEvidence[str]
    trust_badges: FieldEvidence[List[str]]
    related_products_present: FieldEvidence[bool]
    recently_viewed_present: FieldEvidence[bool]
    faq_present: FieldEvidence[bool]

class CartEvidence(BaseModel):
    """Evidence extracted from the Shopify cart drawer or page."""
    url: str
    accessible: bool = Field(True, description="Whether the cart could be inspected.")
    reason: Optional[str] = Field(None, description="Reason if cart is inaccessible.")
    checkout_cta: FieldEvidence[str]
    payment_icons: FieldEvidence[List[str]]
    coupon_field_present: FieldEvidence[bool]
    free_shipping_progress: FieldEvidence[str]
    upsells_present: FieldEvidence[bool]

class AuditEvidence(BaseModel):
    """The complete structured evidence payload sent to the LLM."""
    homepage: HomepageEvidence
    collections: List[CollectionEvidence]
    products: List[ProductEvidence]
    cart: CartEvidence
