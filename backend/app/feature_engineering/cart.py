from app.schemas.evidence import CartEvidence, FieldEvidence, ExtractionStatus
from app.feature_engineering.models import CartFeatures, BusinessFeature
from app.feature_engineering.homepage import build_business_feature

def extract_cart_features(evidence: CartEvidence) -> CartFeatures:
    def check_present(field: FieldEvidence) -> bool:
        if field.status == ExtractionStatus.FOUND:
            if isinstance(field.value, bool):
                return field.value
            return bool(field.value)
        return False

    return CartFeatures(
        coupon_field_present=build_business_feature(evidence.coupon_field_present, evidence.url, check_present(evidence.coupon_field_present)),
        checkout_cta_present=build_business_feature(evidence.checkout_cta, evidence.url, check_present(evidence.checkout_cta)),
        payment_icons_present=build_business_feature(evidence.payment_icons, evidence.url, check_present(evidence.payment_icons)),
        upsells_present=build_business_feature(evidence.upsells_present, evidence.url, check_present(evidence.upsells_present)),
        free_shipping_progress_present=build_business_feature(evidence.free_shipping_progress, evidence.url, check_present(evidence.free_shipping_progress))
    )
