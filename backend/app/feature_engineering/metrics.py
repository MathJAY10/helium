from app.schemas.evidence import AuditEvidence, ExtractionStatus
from app.feature_engineering.models import QualityMetrics

def calculate_quality_metrics(evidence: AuditEvidence, pages_discovered: int) -> QualityMetrics:
    pages_crawled = 1 + len(evidence.collections) + len(evidence.products) + (1 if evidence.cart else 0)
    pages_parsed = pages_crawled # In this version, all crawled pages are parsed
    
    homepage_coverage = 1.0 # Simplify for now
    collection_coverage = 1.0 if len(evidence.collections) > 0 else 0.0
    pdp_coverage = 1.0 if len(evidence.products) > 0 else 0.0
    cart_coverage = 1.0 if evidence.cart and evidence.cart.accessible else 0.0
    
    missing_critical_features = []
    if len(evidence.products) == 0:
        missing_critical_features.append("Products")
        
    return QualityMetrics(
        pages_discovered=pages_discovered,
        pages_crawled=pages_crawled,
        pages_parsed=pages_parsed,
        homepage_coverage=homepage_coverage,
        collection_coverage=collection_coverage,
        pdp_coverage=pdp_coverage,
        cart_coverage=cart_coverage,
        evidence_completeness_score=0.9,
        parser_success_rate=1.0,
        missing_critical_features=missing_critical_features,
        extraction_failures=0
    )
