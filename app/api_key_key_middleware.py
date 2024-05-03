from fastapi import Request
from fastapi.responses import Response

class APIKeyMiddleware:
    def __init__(self, app, api_key: str):
        self.app = app
        self.api_key = api_key

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        path = request.url.path

        # Check API key only for specific paths
        if path in ["/asr", "/detect-language"]:
            api_key_header = request.headers.get("Authorization")
            if not api_key_header or api_key_header != self.api_key:
                response = Response("Invalid API key", status_code=401)
                await response(scope, receive, send)
                return

        # Proceed with the request if the path does not need API key verification or if it is valid
        await self.app(scope, receive, send)