from app.schemas.evidence import AuditEvidence
from app.feature_engineering.models import FeatureSet
from app.feature_engineering.homepage import extract_homepage_features
from app.feature_engineering.collection import extract_collection_features
from app.feature_engineering.product import extract_product_features
from app.feature_engineering.cart import extract_cart_features
from app.feature_engineering.metrics import calculate_quality_metrics
from app.feature_engineering.payload_builder import build_llm_payload

class FeatureEngineer:
    @staticmethod
    def process(evidence: AuditEvidence) -> FeatureSet:
        homepage = extract_homepage_features(evidence.homepage)
        collections = [extract_collection_features(c) for c in evidence.collections]
        products = [extract_product_features(p) for p in evidence.products]
        cart = extract_cart_features(evidence.cart)
        
        # In a real system, pages_discovered would be passed from crawler
        pages_discovered = 1 + len(evidence.collections) + len(evidence.products) + 1
        metrics = calculate_quality_metrics(evidence, pages_discovered)
        
        feature_set = FeatureSet(
            homepage=homepage,
            collections=collections,
            products=products,
            cart=cart,
            metadata={"store_url": evidence.homepage.url},
            quality_metrics=metrics,
            llm_payload=""
        )
        
        feature_set.llm_payload = build_llm_payload(feature_set)
        return feature_set
