from pydantic import BaseModel, HttpUrl, field_validator
from urllib.parse import urlparse
import ipaddress

class AuditRequest(BaseModel):
    url: HttpUrl

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: HttpUrl):
        parsed = urlparse(str(v))
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL must use HTTP or HTTPS")
        
        hostname = parsed.hostname
        if not hostname:
            raise ValueError("Invalid URL format")
            
        if hostname == "localhost" or hostname.endswith(".local"):
            raise ValueError("Localhost URLs are not allowed")
            
        is_ip = False
        try:
            ip = ipaddress.ip_address(hostname)
            is_ip = True
        except ValueError:
            pass # Not an IP address, normal hostname
            
        if is_ip and (ip.is_private or ip.is_loopback):
            raise ValueError("Private IP addresses are not allowed")
            
        return v
