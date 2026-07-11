from app.schemas.evidence import ProductEvidence, FieldEvidence, ExtractionStatus
from app.feature_engineering.models import ProductFeatures, BusinessFeature
from app.feature_engineering.homepage import build_business_feature

def extract_product_features(evidence: ProductEvidence) -> ProductFeatures:
    def check_present(field: FieldEvidence) -> bool:
        if field.status == ExtractionStatus.FOUND:
            if isinstance(field.value, bool):
                return field.value
            return bool(field.value)
        return False

    # Derived Features
    reviews_present = False
    if evidence.review_count.status == ExtractionStatus.FOUND and evidence.review_count.value and evidence.review_count.value > 0:
        reviews_present = True

    discount_present = False
    if evidence.discount_percentage.status == ExtractionStatus.FOUND and evidence.discount_percentage.value:
        discount_present = True

    multiple_images_present = False
    if evidence.image_count.status == ExtractionStatus.FOUND and evidence.image_count.value and evidence.image_count.value > 1:
        multiple_images_present = True

    return ProductFeatures(
        reviews_present=build_business_feature(evidence.review_count, evidence.url, reviews_present),
        rating_present=build_business_feature(evidence.rating, evidence.url, check_present(evidence.rating)),
        shipping_information_present=build_business_feature(evidence.shipping_text, evidence.url, check_present(evidence.shipping_text)),
        returns_information_present=build_business_feature(evidence.returns_text, evidence.url, check_present(evidence.returns_text)),
        sticky_add_to_cart_present=build_business_feature(evidence.sticky_add_to_cart, evidence.url, check_present(evidence.sticky_add_to_cart)),
        size_guide_present=build_business_feature(evidence.size_guide_present, evidence.url, check_present(evidence.size_guide_present)),
        related_products_present=build_business_feature(evidence.related_products_present, evidence.url, check_present(evidence.related_products_present)),
        recently_viewed_present=build_business_feature(evidence.recently_viewed_present, evidence.url, check_present(evidence.recently_viewed_present)),
        faq_present=build_business_feature(evidence.faq_present, evidence.url, check_present(evidence.faq_present)),
        discount_present=build_business_feature(evidence.discount_percentage, evidence.url, discount_present),
        variants_present=build_business_feature(evidence.variants_present, evidence.url, check_present(evidence.variants_present)),
        multiple_images_present=build_business_feature(evidence.image_count, evidence.url, multiple_images_present),
        videos_present=build_business_feature(evidence.video_present, evidence.url, check_present(evidence.video_present))
    )
