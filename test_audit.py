import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

from app.services.audit_service import AuditService
from app.utils.config import get_settings

async def main():
    settings = get_settings()
    service = AuditService(settings)
    try:
        res = await service.run_audit("https://gymshark.com", "test_req")
        print("Success!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
