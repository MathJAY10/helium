from app.parser.common import BaseParser
from app.parser.utils import extract_text_from_selectors, extract_list_from_selectors
from app.parser import selectors
from app.schemas.evidence import ProductEvidence, ConfidenceLevel

class ProductParser(BaseParser):
    def parse(self) -> ProductEvidence:
        title = extract_text_from_selectors(self.soup, selectors.PRODUCT_TITLE)
        
        # Product JSON-LD gives great confidence for price, brand, currency
        brand = None
        price = None
        currency = None
        review_count = None
        rating = None
        
        for block in self.json_ld:
            if block.get("@type") == "Product":
                if isinstance(block.get("brand"), dict):
                    brand = block["brand"].get("name")
                
                offers = block.get("offers")
                if offers:
                    if isinstance(offers, list):
                        offers = offers[0]
                    price = str(offers.get("price", ""))
                    currency = offers.get("priceCurrency")
                
                reviews = block.get("aggregateRating")
                if reviews:
                    rating = str(reviews.get("ratingValue", ""))
                    review_count = int(reviews.get("reviewCount", 0))

        # Fallbacks for DOM
        if not price:
            price = extract_text_from_selectors(self.soup, selectors.PRICE)
        
        compare_at_price = extract_text_from_selectors(self.soup, selectors.COMPARE_AT_PRICE)
        
        # Discount logic
        discount_percentage = None
        if price and compare_at_price:
            import re
            p_match = re.search(r'[\d\.]+', price)
            c_match = re.search(r'[\d\.]+', compare_at_price)
            if p_match and c_match:
                try:
                    p_val = float(p_match.group())
                    c_val = float(c_match.group())
                    if c_val > p_val:
                        discount = ((c_val - p_val) / c_val) * 100
                        discount_percentage = f"{int(discount)}%"
                except ValueError:
                    pass
        
        # Images & Videos
        images = extract_list_from_selectors(self.soup, [".product__media img", ".product-single__media img", "[data-media-id] img"], "src")
        image_count = len(images) if images else 0
        video_present = self.is_present(["video", "iframe[src*='youtube']", "iframe[src*='vimeo']", ".product__media-video"])
        
        # Other Features
        sticky_add_to_cart = self.is_present(selectors.ADD_TO_CART_STICKY)
        variants_present = self.is_present(selectors.VARIANTS)
        size_guide_present = self.is_present(selectors.SIZE_GUIDE)
        
        # Trust badges
        trust_badges = extract_list_from_selectors(self.soup, selectors.TRUST_BADGES, "src")
        
        related_products_present = self.is_present([".product-recommendations", "#shopify-section-product-recommendations", ".related-products"])
        recently_viewed_present = self.is_present([".recently-viewed", "#recently-viewed-products"])
        faq_present = self.is_present([".accordion", ".faq", "summary:contains('FAQ')"])
        
        shipping_text = extract_text_from_selectors(self.soup, [".shipping-policy", "a:contains('Shipping')", "summary:contains('Shipping')"])
        returns_text = extract_text_from_selectors(self.soup, [".return-policy", "a:contains('Return')", "summary:contains('Return')"])

        return ProductEvidence(url=self.url,
            product_title=self.build_field(title),
            brand=self.build_field(brand),
            price=self.build_field(price),
            compare_at_price=self.build_field(compare_at_price),
            discount_percentage=self.build_field(discount_percentage),
            currency=self.build_field(currency),
            rating=self.build_field(rating),
            review_count=self.build_field(review_count),
            image_count=self.build_field(image_count if image_count > 0 else None),
            video_present=self.build_field(video_present),
            sticky_add_to_cart=self.build_field(sticky_add_to_cart),
            variants_present=self.build_field(variants_present),
            size_guide_present=self.build_field(size_guide_present),
            shipping_text=self.build_field(shipping_text),
            returns_text=self.build_field(returns_text),
            trust_badges=self.build_field(list(set(trust_badges)) if trust_badges else None),
            related_products_present=self.build_field(related_products_present),
            recently_viewed_present=self.build_field(recently_viewed_present),
            faq_present=self.build_field(faq_present)
        )
