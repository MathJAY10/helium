from typing import Any, Optional, TypeVar, List
from bs4 import BeautifulSoup
from app.schemas.evidence import FieldEvidence, ExtractionStatus, ConfidenceLevel
from app.parser.utils import extract_json_ld

T = TypeVar('T')

class BaseParser:
    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url
        self.soup = BeautifulSoup(html, "html.parser")
        self.json_ld = extract_json_ld(self.soup)

    def build_field(self, value: Optional[T], confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM) -> FieldEvidence[T]:
        """Wrap an extracted value into FieldEvidence."""
        if value is None or (isinstance(value, list) and len(value) == 0) or (isinstance(value, str) and value.strip() == ""):
            return FieldEvidence(
                value=None,
                status=ExtractionStatus.NOT_FOUND,
                confidence=ConfidenceLevel.HIGH
            )
        return FieldEvidence(
            value=value,
            status=ExtractionStatus.FOUND,
            confidence=confidence
        )

    def is_present(self, selectors: List[str]) -> bool:
        """Check if any element matching the selectors exists."""
        for sel in selectors:
            if self.soup.select_one(sel):
                return True
        return False
