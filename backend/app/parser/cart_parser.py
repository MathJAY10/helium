from app.parser.common import BaseParser
from app.parser.utils import extract_text_from_selectors, extract_list_from_selectors
from app.parser import selectors
from app.schemas.evidence import CartEvidence

class CartParser(BaseParser):
    def parse(self) -> CartEvidence:
        # Check if cart is accessible
        if self.is_present(["[data-cart-empty]", ".cart--empty"]):
            return CartEvidence(url=self.url,
                accessible=False,
                reason="Cart is empty or inaccessible.",
                checkout_cta=self.build_field(None),
                payment_icons=self.build_field(None),
                coupon_field_present=self.build_field(False),
                free_shipping_progress=self.build_field(None),
                upsells_present=self.build_field(False)
            )

        checkout_cta = extract_text_from_selectors(self.soup, selectors.CHECKOUT_CTA)
        payment_icons = extract_list_from_selectors(self.soup, selectors.TRUST_BADGES, "src")
        coupon_field_present = self.is_present(selectors.COUPON_FIELD)
        
        free_shipping_progress = extract_text_from_selectors(self.soup, [".free-shipping-bar", ".shipping-progress", "[data-free-shipping]"])
        upsells_present = self.is_present([".cart-upsell", ".cart-recommendations", "[data-cart-upsell]"])

        return CartEvidence(url=self.url,
            accessible=True,
            reason=None,
            checkout_cta=self.build_field(checkout_cta),
            payment_icons=self.build_field(list(set(payment_icons)) if payment_icons else None),
            coupon_field_present=self.build_field(coupon_field_present),
            free_shipping_progress=self.build_field(free_shipping_progress),
            upsells_present=self.build_field(upsells_present)
        )
