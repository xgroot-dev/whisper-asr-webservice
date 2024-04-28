from fastapi import Request, Response

class APIKeyMiddleware:
    def __init__(self, app, api_key: str):
        self.app = app
        self.api_key = api_key

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive)
        api_key_header = request.headers.get("Authorization")

        if not api_key_header or api_key_header != self.api_key:
            return Response(status_code=401, content="Invalid API key")

        return await self.app(scope, receive, send)
