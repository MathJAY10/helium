import time
import asyncio
import logging
from app.utils.config import Settings
from app.crawler.crawler import ShopifyCrawler
from app.parser.orchestrator import EvidenceParser
from app.feature_engineering.aggregator import FeatureEngineer
from app.llm.gemini_client import GeminiClient
from app.ranking.engine import RankingEngine
from app.ranking.models import RankedAudit
from app.schemas.responses import AuditResponse, AuditMetadata
from app.utils.exceptions import CROEngineException
from app.utils.logger import get_logger

logger = get_logger()

class AuditService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def run_audit(self, url: str, request_id: str) -> AuditResponse:
        total_start = time.time()
        timings = {}

        try:
            # 1. Crawl
            t0 = time.time()
            
            def _run_crawler_sync(target_url):
                import sys
                if sys.platform == "win32":
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                crawler = ShopifyCrawler()
                try:
                    loop.run_until_complete(crawler.start())
                    return loop.run_until_complete(crawler.crawl_store(target_url))
                finally:
                    loop.run_until_complete(crawler.stop())
                    loop.close()

            pages = await asyncio.to_thread(_run_crawler_sync, url)
            timings["crawl_ms"] = round((time.time() - t0) * 1000)

            if not pages or not pages.homepage:
                raise CROEngineException("Crawler returned no pages", 503, "CRAWLER_FAILED")

            # 2. Parse
            t0 = time.time()
            evidence = EvidenceParser.parse(pages)
            timings["parse_ms"] = round((time.time() - t0) * 1000)

            # 3. Feature Engineering
            t0 = time.time()
            feature_set = FeatureEngineer.process(evidence)
            timings["feature_ms"] = round((time.time() - t0) * 1000)

            # 4. LLM
            t0 = time.time()
            llm_client = GeminiClient()
            validated_audit = await llm_client.analyze_features(feature_set)
            timings["llm_ms"] = round((time.time() - t0) * 1000)

            # 5. Ranking
            t0 = time.time()
            ranked_audit = RankingEngine.process(validated_audit, feature_set.quality_metrics)
            timings["ranking_ms"] = round((time.time() - t0) * 1000)

            timings["total_ms"] = round((time.time() - total_start) * 1000)
            logger.info(f"Audit Complete | request_id={request_id} url={url} timings={timings}")

            return AuditResponse(
                audit=ranked_audit,
                metadata=AuditMetadata(
                    url=url,
                    duration_ms=timings["total_ms"],
                    evidence_completeness=feature_set.quality_metrics.evidence_completeness_score,
                    parser_success_rate=feature_set.quality_metrics.parser_success_rate
                )
            )

        except asyncio.TimeoutError:
            logger.error(f"Audit Timeout | request_id={request_id} url={url}")
            raise CROEngineException("Request timed out during audit execution", 408, "TIMEOUT")
        except CROEngineException:
            raise
        except Exception as e:
            logger.exception(f"Audit failed unexpectedly: {repr(e)}")
            raise CROEngineException(f"Internal server error: {repr(e)}", 500, "INTERNAL_ERROR")
