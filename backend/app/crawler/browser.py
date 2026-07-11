import os
from playwright.async_api import async_playwright, BrowserContext

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/119.0.0.0 Safari/537.36"
)

VIEWPORT = {"width": 1920, "height": 1080}

EXTRA_HTTP_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

class BrowserManager:
    """
    Manages the Playwright browser instance and context to ensure realistic headers and avoid basic bot detection.
    """
    def __init__(self):
        self._playwright = None
        self._browser = None

    async def start(self):
        self._playwright = await async_playwright().start()
        # Launch chromium. Set headless=True for production, but headless=new is preferred if supported.
        self._browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def create_context(self) -> BrowserContext:
        """
        Creates a new browser context with realistic fingerprinting.
        """
        if not self._browser:
            raise RuntimeError("Browser not started. Call start() first.")
        
        context = await self._browser.new_context(
            user_agent=USER_AGENT,
            viewport=VIEWPORT,
            extra_http_headers=EXTRA_HTTP_HEADERS,
            bypass_csp=True,
            ignore_https_errors=True
        )
        
        # Adding a small script to hide playwright footprint
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        return context
