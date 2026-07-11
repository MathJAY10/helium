from app.schemas.evidence import CollectionEvidence, FieldEvidence, ExtractionStatus
from app.feature_engineering.models import CollectionFeatures, BusinessFeature
from app.feature_engineering.homepage import build_business_feature

def extract_collection_features(evidence: CollectionEvidence) -> CollectionFeatures:
    def check_present(field: FieldEvidence) -> bool:
        if field.status == ExtractionStatus.FOUND:
            if isinstance(field.value, bool):
                return field.value
            return bool(field.value)
        return False

    return CollectionFeatures(
        filters_present=build_business_feature(evidence.filters_present, evidence.url, check_present(evidence.filters_present)),
        sorting_present=build_business_feature(evidence.sorting_present, evidence.url, check_present(evidence.sorting_present)),
        sale_badges_present=build_business_feature(evidence.sale_badges, evidence.url, check_present(evidence.sale_badges)),
        pagination_present=build_business_feature(evidence.pagination_present, evidence.url, check_present(evidence.pagination_present))
    )
