from app.parser.common import BaseParser
from app.parser.utils import extract_text_from_selectors, extract_list_from_selectors
from app.parser import selectors
from app.schemas.evidence import HomepageEvidence, ConfidenceLevel

class HomepageParser(BaseParser):
    def parse(self) -> HomepageEvidence:
        hero_heading = extract_text_from_selectors(self.soup, selectors.HERO_HEADING)
        hero_cta = extract_text_from_selectors(self.soup, selectors.HERO_CTA)
        announcement_bar = extract_text_from_selectors(self.soup, selectors.ANNOUNCEMENT_BAR)
        
        # Navigation links are usually inside header or nav
        nav_links = extract_list_from_selectors(self.soup, ["header nav a", ".site-nav a", ".header__menu-item"])
        
        # Featured collections
        featured_collections = extract_list_from_selectors(self.soup, [".collection-list__item", ".card__heading", ".collection-card"])
        
        # Newsletter
        newsletter_present = self.is_present(["form[action*='/contact']", "input[name='contact[email]']", ".newsletter-form"])
        
        # Trust Badges
        trust_badges = extract_list_from_selectors(self.soup, selectors.TRUST_BADGES, attribute="src")
        
        # Social links
        social_links = extract_list_from_selectors(self.soup, selectors.SOCIAL_LINKS, attribute="href")

        return HomepageEvidence(url=self.url,
            hero_heading=self.build_field(hero_heading),
            hero_cta=self.build_field(hero_cta),
            announcement_bar=self.build_field(announcement_bar),
            navigation_links=self.build_field(list(set(nav_links)) if nav_links else None),
            featured_collections=self.build_field(list(set(featured_collections)) if featured_collections else None),
            newsletter_present=self.build_field(newsletter_present, ConfidenceLevel.HIGH if newsletter_present else ConfidenceLevel.MEDIUM),
            trust_badges=self.build_field(trust_badges),
            social_links=self.build_field(social_links)
        )
