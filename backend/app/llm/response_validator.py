import pydantic
from app.llm.models import ValidatedAudit
from app.llm.exceptions import LLMValidationError

class ResponseValidator:
    @staticmethod
    def validate(response_text: str) -> ValidatedAudit:
        try:
            # Clean up potential markdown wrappers
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            return ValidatedAudit.model_validate_json(text)
        except pydantic.ValidationError as e:
            raise LLMValidationError(f"Response validation failed: {e}")
        except Exception as e:
            raise LLMValidationError(f"Unexpected error during validation: {e}")
