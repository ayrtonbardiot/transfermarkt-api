from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.settings import settings

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/docs" or request.url.path.startswith("/openapi.json"):
            response = await call_next(request)
            return response

        api_key = request.headers.get("x-api-key")
        
        if api_key != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        response = await call_next(request)
        return response