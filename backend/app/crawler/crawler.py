import asyncio
import os
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext, TimeoutError as PlaywrightTimeoutError

from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.crawler.models import PageResult, StoreResult, PageType
from app.crawler.exceptions import BotProtectionError, MaxRetriesExceededError, CrawlerError
from app.crawler.browser import BrowserManager
from app.crawler.cache import crawler_cache

logger = get_logger()
settings = get_settings()

SCREENSHOT_DIR = os.path.join(os.getcwd(), "artifacts", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class ShopifyCrawler:
    """
    Asynchronous crawler for Shopify stores using Playwright.
    """
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_PAGES)
    
    async def start(self):
        await self.browser_manager.start()

    async def stop(self):
        await self.browser_manager.stop()

    def _normalize_url(self, base_url: str, href: str) -> str:
        """Normalizes an href against the base URL, removing fragments."""
        if not href:
            return ""
        url = urljoin(base_url, href)
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def _is_valid_internal_link(self, base_domain: str, url: str) -> bool:
        """Checks if a URL is an internal link and not a social or protocol link."""
        if not url:
            return False
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if parsed.netloc:
            netloc = parsed.netloc.replace("www.", "")
            base = base_domain.replace("www.", "")
            if netloc != base:
                return False
        # Ignore common social/external identifiers
        ignored_substrings = ["instagram.com", "facebook.com", "twitter.com", "tiktok.com", "pinterest.com"]
        if any(sub in url for sub in ignored_substrings):
            return False
        return True

    async def _fetch_page(self, context: BrowserContext, url: str, page_type: PageType, retries: int = 3) -> PageResult:
        """
        Fetches a page with exponential backoff and caching.
        """
        cached = crawler_cache.get(url)
        if cached:
            logger.info("Cache hit", url=url, type=page_type.value)
            return cached

        logger.info("Crawling page", url=url, type=page_type.value)
        start_time = time.time()
        
        for attempt in range(1, retries + 1):
            page = await context.new_page()
            try:
                # Use domcontentloaded instead of networkidle to prevent timeouts on tracking-heavy sites
                response = await page.goto(url, timeout=settings.REQUEST_TIMEOUT * 1000, wait_until="domcontentloaded")
                
                # Check for bot protection (e.g. Cloudflare Challenge)
                if response and response.status in (403, 503):
                    content = await page.content()
                    if "cloudflare" in content.lower() or "challenge" in content.lower():
                        raise BotProtectionError(f"Bot protection detected on {url}")

                html = await page.content()
                
                # Take screenshot
                safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
                screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{page_type.value.lower()}.png")
                await page.screenshot(path=screenshot_path, full_page=True)
                
                duration = int((time.time() - start_time) * 1000)
                
                result = PageResult(
                    url=url,
                    page_type=page_type,
                    status="success",
                    html=html,
                    screenshot_path=screenshot_path,
                    response_time_ms=duration
                )
                
                crawler_cache.set(url, result)
                logger.info("Crawl finished", url=url, duration_ms=duration)
                return result

            except PlaywrightTimeoutError:
                logger.warning(f"Timeout on {url}, attempt {attempt}/{retries}")
                if attempt == retries:
                    duration = int((time.time() - start_time) * 1000)
                    return PageResult(
                        url=url, page_type=page_type, status="timeout", 
                        response_time_ms=duration, error_reason="Timeout exceeded"
                    )
                await asyncio.sleep(2 ** attempt) # Exponential backoff
            except BotProtectionError as e:
                logger.error(f"Blocked by bot protection: {e}")
                duration = int((time.time() - start_time) * 1000)
                return PageResult(
                    url=url, page_type=page_type, status="blocked", 
                    response_time_ms=duration, error_reason="bot_protection"
                )
            except Exception as e:
                logger.warning(f"Error on {url}: {e}, attempt {attempt}/{retries}")
                if attempt == retries:
                    duration = int((time.time() - start_time) * 1000)
                    return PageResult(
                        url=url, page_type=page_type, status="error", 
                        response_time_ms=duration, error_reason=str(e)
                    )
                await asyncio.sleep(2 ** attempt)
            finally:
                await page.close()
        
        raise MaxRetriesExceededError(f"Failed to fetch {url} after {retries} attempts.")

    def discover_links(self, base_url: str, html: str) -> tuple[list[str], list[str]]:
        """
        Discovers collection and product links from homepage HTML.
        Returns (collections, products) limited to 1 collection, 5 products.
        """
        soup = BeautifulSoup(html, "html.parser")
        base_domain = urlparse(base_url).netloc
        
        collections = set()
        products = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            url = self._normalize_url(base_url, href)
            
            if not self._is_valid_internal_link(base_domain, url):
                continue
                
            if "/collections/" in url and "/products/" not in url:
                collections.add(url)
            elif "/products/" in url:
                products.add(url)
        
        # Strict limits to stay within Render's 30-second free-tier timeout
        return list(collections)[:0], list(products)[:2]

    async def _crawl_bounded(self, context: BrowserContext, url: str, page_type: PageType) -> PageResult:
        """Wraps fetch with a semaphore for concurrency control."""
        async with self.semaphore:
            return await self._fetch_page(context, url, page_type)

    async def crawl_store(self, base_url: str) -> StoreResult:
        """
        Main entry point to crawl the entire store.
        """
        logger.info("Starting store crawl", store=base_url)
        context = await self.browser_manager.create_context()
        
        try:
            # 1. Crawl Homepage
            homepage_result = await self._crawl_bounded(context, base_url, PageType.HOMEPAGE)
            
            if homepage_result.status != "success" or not homepage_result.html:
                logger.error("Homepage crawl failed. Aborting store crawl.")
                return StoreResult(homepage=homepage_result)

            # 2. Discover Links
            collection_urls, product_urls = self.discover_links(base_url, homepage_result.html)
            cart_url = self._normalize_url(base_url, "/cart")
            
            logger.info("Discovery complete", collections=len(collection_urls), products=len(product_urls))

            # 3. Crawl concurrently (Products only - skip cart to stay within timeout)
            tasks = []
            for url in product_urls:
                tasks.append(self._crawl_bounded(context, url, PageType.PRODUCT))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            store_result = StoreResult(homepage=homepage_result)
            
            for res in results:
                if isinstance(res, PageResult):
                    if res.page_type == PageType.COLLECTION:
                        store_result.collections.append(res)
                    elif res.page_type == PageType.PRODUCT:
                        store_result.products.append(res)
                    elif res.page_type == PageType.CART:
                        store_result.cart = res
                else:
                    logger.error("Crawl task raised an exception", error=str(res))
                    
            logger.info("Store crawl complete", store=base_url)
            return store_result

        finally:
            await context.close()
