import sys
import os
import asyncio

# Force Playwright to look for browsers in the Render preserved folder
if "RENDER" in os.environ:
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/opt/render/project/playwright"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, audit
from app.utils.middleware import RequestTracingMiddleware
from app.utils.exceptions import CROEngineException
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="Shopify CRO Opportunity Engine",
    description="Generates prioritized Conversion Rate Optimization (CRO) audits using deterministic extraction and LLM reasoning.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Tracing and Timing
app.add_middleware(RequestTracingMiddleware)

# Routes
app.include_router(health.router)
app.include_router(audit.router)

# Exception Handlers
@app.exception_handler(CROEngineException)
async def cro_engine_exception_handler(request: Request, exc: CROEngineException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred.",
            "details": {}
        }
    )
