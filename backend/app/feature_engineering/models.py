from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from app.schemas.evidence import ExtractionStatus, ConfidenceLevel

class BusinessFeature(BaseModel):
    value: Any
    status: ExtractionStatus
    confidence: ConfidenceLevel
    source: str
    page_url: str

class HomepageFeatures(BaseModel):
    hero_cta_present: BusinessFeature
    announcement_bar_present: BusinessFeature
    newsletter_present: BusinessFeature
    social_links_present: BusinessFeature
    navigation_present: BusinessFeature
    featured_collections_present: BusinessFeature
    trust_badges_present: BusinessFeature

class CollectionFeatures(BaseModel):
    filters_present: BusinessFeature
    sorting_present: BusinessFeature
    sale_badges_present: BusinessFeature
    pagination_present: BusinessFeature

class ProductFeatures(BaseModel):
    reviews_present: BusinessFeature
    rating_present: BusinessFeature
    shipping_information_present: BusinessFeature
    returns_information_present: BusinessFeature
    sticky_add_to_cart_present: BusinessFeature
    size_guide_present: BusinessFeature
    related_products_present: BusinessFeature
    recently_viewed_present: BusinessFeature
    faq_present: BusinessFeature
    discount_present: BusinessFeature
    variants_present: BusinessFeature
    multiple_images_present: BusinessFeature
    videos_present: BusinessFeature

class CartFeatures(BaseModel):
    coupon_field_present: BusinessFeature
    checkout_cta_present: BusinessFeature
    payment_icons_present: BusinessFeature
    upsells_present: BusinessFeature
    free_shipping_progress_present: BusinessFeature

class QualityMetrics(BaseModel):
    pages_discovered: int
    pages_crawled: int
    pages_parsed: int
    homepage_coverage: float
    collection_coverage: float
    pdp_coverage: float
    cart_coverage: float
    evidence_completeness_score: float
    parser_success_rate: float
    missing_critical_features: List[str]
    extraction_failures: int

class FeatureSet(BaseModel):
    homepage: HomepageFeatures
    collections: List[CollectionFeatures]
    products: List[ProductFeatures]
    cart: CartFeatures
    metadata: Dict[str, Any]
    quality_metrics: QualityMetrics
    llm_payload: str
