"""Centralized CSS selectors and XPath-like patterns for parsing."""

# Common Shopify Selectors
JSON_LD_SELECTOR = "script[type='application/ld+json']"

# Homepage
HERO_HEADING = [
    "h1",
    ".hero__title",
    ".banner__heading",
    "[data-section-type='hero'] h2"
]

HERO_CTA = [
    ".hero__btn",
    ".banner__buttons a",
    ".hero a.btn",
    "[data-section-type='hero'] a.button"
]

ANNOUNCEMENT_BAR = [
    ".announcement-bar",
    "#shopify-section-announcement-bar",
    "[data-section-type='announcement-bar']"
]

TRUST_BADGES = [
    "img[src*='trust']",
    "img[src*='secure']",
    "img[src*='guarantee']",
    ".trust-badge",
    ".payment-icons"
]

SOCIAL_LINKS = [
    "a[href*='instagram.com']",
    "a[href*='facebook.com']",
    "a[href*='twitter.com']",
    "a[href*='tiktok.com']",
    "a[href*='youtube.com']"
]

# Collection
FILTERS = [
    ".facets",
    ".collection-filters",
    "#FacetFiltersForm",
    ".filter-group"
]

SORTING = [
    ".sort-by",
    "select[name='sort_by']",
    "#SortBy"
]

SALE_BADGES = [
    ".badge--sale",
    ".price--on-sale .badge",
    ".product-tag--sale"
]

PAGINATION = [
    ".pagination",
    "nav.pagination",
    ".paginate"
]

# Product
PRICE = [
    ".price-item--regular",
    ".product__price",
    "[data-product-price]"
]

COMPARE_AT_PRICE = [
    ".price-item--sale",
    "s.price-item",
    "[data-compare-price]"
]

PRODUCT_TITLE = [
    "h1.product__title",
    ".product-single__title",
    "h1"
]

ADD_TO_CART_STICKY = [
    ".product-form--sticky",
    "[data-sticky-add-to-cart]"
]

SIZE_GUIDE = [
    ".size-chart-link",
    "a:contains('Size Guide')",
    "a:contains('Size Chart')"
]

VARIANTS = [
    "variant-radios",
    "variant-selects",
    ".product-form__variants",
    "select[name='id']"
]

# Cart
CHECKOUT_CTA = [
    "button[name='checkout']",
    ".cart__checkout-button",
    "#checkout"
]

COUPON_FIELD = [
    "input[name='discount']",
    "#discount",
    ".cart-discount"
]
