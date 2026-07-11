from app.schemas.evidence import HomepageEvidence, FieldEvidence, ExtractionStatus
from app.feature_engineering.models import HomepageFeatures, BusinessFeature

def build_business_feature(field: FieldEvidence, page_url: str, is_present: bool) -> BusinessFeature:
    return BusinessFeature(
        value=is_present,
        status=field.status,
        confidence=field.confidence,
        source="Parser",
        page_url=page_url
    )

def extract_homepage_features(evidence: HomepageEvidence) -> HomepageFeatures:
    def check_present(field: FieldEvidence) -> bool:
        if field.status == ExtractionStatus.FOUND:
            if isinstance(field.value, bool):
                return field.value
            return bool(field.value)
        return False

    return HomepageFeatures(
        hero_cta_present=build_business_feature(evidence.hero_cta, evidence.url, check_present(evidence.hero_cta)),
        announcement_bar_present=build_business_feature(evidence.announcement_bar, evidence.url, check_present(evidence.announcement_bar)),
        newsletter_present=build_business_feature(evidence.newsletter_present, evidence.url, check_present(evidence.newsletter_present)),
        social_links_present=build_business_feature(evidence.social_links, evidence.url, check_present(evidence.social_links)),
        navigation_present=build_business_feature(evidence.navigation_links, evidence.url, check_present(evidence.navigation_links)),
        featured_collections_present=build_business_feature(evidence.featured_collections, evidence.url, check_present(evidence.featured_collections)),
        trust_badges_present=build_business_feature(evidence.trust_badges, evidence.url, check_present(evidence.trust_badges))
    )
