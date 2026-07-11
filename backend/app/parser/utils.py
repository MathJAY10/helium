import json
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.parser.selectors import JSON_LD_SELECTOR

def extract_json_ld(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract all JSON-LD blocks from the page."""
    json_ld_data = []
    scripts = soup.select(JSON_LD_SELECTOR)
    for script in scripts:
        if script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    json_ld_data.extend(data)
                elif isinstance(data, dict):
                    json_ld_data.append(data)
            except json.JSONDecodeError:
                continue
    return json_ld_data

def clean_text(text: Optional[str]) -> Optional[str]:
    """Clean extra whitespace from text."""
    if not text:
        return None
    cleaned = " ".join(text.split())
    return cleaned if cleaned else None

def extract_text_from_selectors(soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
    """Try a list of selectors and return text from the first one that matches."""
    for selector in selectors:
        element = soup.select_one(selector)
        if element and element.text:
            cleaned = clean_text(element.text)
            if cleaned:
                return cleaned
    return None

def extract_list_from_selectors(soup: BeautifulSoup, selectors: List[str], attribute: str = None) -> List[str]:
    """Try a list of selectors and return all matches from the first one that yields results."""
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            results = []
            for el in elements:
                if attribute:
                    val = el.get(attribute)
                    if val:
                        results.append(val.strip())
                else:
                    text = clean_text(el.text)
                    if text:
                        results.append(text)
            if results:
                return results
    return []
