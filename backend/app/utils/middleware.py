import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import get_logger

logger = get_logger()

class RequestTracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        logger.info(f"Request started | request_id={request_id} method={request.method} url={request.url.path}")
        
        try:
            response = await call_next(request)
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.exception(f"Request failed | request_id={request_id} method={request.method} url={request.url.path} duration_ms={duration:.2f} error={str(e)}")
            raise

        duration = (time.time() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.2f}ms"
        
        logger.info(f"Request completed | request_id={request_id} status={response.status_code} duration_ms={duration:.2f}")
        
        return response
