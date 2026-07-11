import asyncio
import time
from google import genai
from google.genai import types

from app.utils.config import get_settings
from app.utils.logger import get_logger
from app.feature_engineering.models import FeatureSet
from app.llm.prompt_builder import PromptBuilder
from app.llm.response_validator import ResponseValidator
from app.llm.models import ValidatedAudit
from app.llm.retry import retry_llm_call
from app.llm.exceptions import LLMValidationError

settings = get_settings()
logger = get_logger()

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
        
    @retry_llm_call(max_retries=3, initial_backoff=2.0)
    async def analyze_features(self, feature_set: FeatureSet) -> ValidatedAudit:
        system_prompt = PromptBuilder.build_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(feature_set.llm_payload)
        
        logger.info("Calling Gemini API", model=self.model_name)
        start_time = time.time()
        
        def _call_sync():
            return self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=ValidatedAudit,
                ),
            )

        try:
            # Using to_thread for safe async wrapping
            response = await asyncio.to_thread(_call_sync)
        except Exception as e:
            logger.error("Gemini API call failed", error=str(e))
            raise
            
        duration = time.time() - start_time
        usage = response.usage_metadata
        
        logger.info(
            "Gemini Call Complete",
            duration_s=round(duration, 2),
            prompt_tokens=usage.prompt_token_count if usage else None,
            candidates_tokens=usage.candidates_token_count if usage else None,
            total_tokens=usage.total_token_count if usage else None,
        )
        
        try:
            validated = ResponseValidator.validate(response.text)
            return validated
        except LLMValidationError as e:
            logger.error("LLM Validation Error", error=str(e), response_text=response.text)
            raise
