from app.parser.common import BaseParser
from app.parser.utils import extract_text_from_selectors, extract_list_from_selectors
from app.parser import selectors
from app.schemas.evidence import CollectionEvidence, ConfidenceLevel

class CollectionParser(BaseParser):
    def parse(self) -> CollectionEvidence:
        title = extract_text_from_selectors(self.soup, ["h1.collection-hero__title", "h1.collection-title", "h1"])
        
        filters_present = self.is_present(selectors.FILTERS)
        sorting_present = self.is_present(selectors.SORTING)
        pagination_present = self.is_present(selectors.PAGINATION)
        
        # Product count
        product_count_str = extract_text_from_selectors(self.soup, ["#ProductCount", ".collection-product-count", "[data-product-count]"])
        product_count = None
        if product_count_str:
            import re
            match = re.search(r'\d+', product_count_str)
            if match:
                product_count = int(match.group())
        else:
            # Fallback to counting elements
            elements = self.soup.select(".grid__item, .product-grid-item, .collection__item")
            if elements:
                product_count = len(elements)
        
        sale_badges = extract_list_from_selectors(self.soup, selectors.SALE_BADGES)

        return CollectionEvidence(url=self.url,
            collection_title=self.build_field(title),
            filters_present=self.build_field(filters_present),
            sorting_present=self.build_field(sorting_present),
            product_count=self.build_field(product_count),
            sale_badges=self.build_field(list(set(sale_badges)) if sale_badges else None),
            pagination_present=self.build_field(pagination_present)
        )
