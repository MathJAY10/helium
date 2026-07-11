from typing import List
from app.crawler.models import StoreResult
from app.schemas.evidence import AuditEvidence
from app.parser.homepage_parser import HomepageParser
from app.parser.collection_parser import CollectionParser
from app.parser.product_parser import ProductParser
from app.parser.cart_parser import CartParser

class EvidenceParser:
    """Orchestrates parsing across the entire store crawl result."""
    
    @staticmethod
    def parse(store_result: StoreResult) -> AuditEvidence:
        homepage = HomepageParser(store_result.homepage.html, store_result.homepage.url).parse()
        
        collections = []
        for col in store_result.collections:
            if col.html:
                collections.append(CollectionParser(col.html, col.url).parse())
                
        products = []
        for prod in store_result.products:
            if prod.html:
                products.append(ProductParser(prod.html, prod.url).parse())
                
        if store_result.cart and store_result.cart.html:
            cart = CartParser(store_result.cart.html, store_result.cart.url).parse()
        else:
            cart = CartParser("", "").parse()

        return AuditEvidence(
            homepage=homepage,
            collections=collections,
            products=products,
            cart=cart
        )
