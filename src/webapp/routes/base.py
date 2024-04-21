from aiohttp import web
import functools

def require_headers(required_headers):
    def wrapper(handler):
        @functools.wraps(handler)
        async def wrapped_handler(request):
            header_errors = []
            for header, expected_value in required_headers.items():
                actual_value = request.headers.get(header)
                if actual_value != expected_value:
                    header_errors.append(f"headers check fall")

            if header_errors:
                return web.Response(status=400, text="; ".join(header_errors))
            return await handler(request)
        return wrapped_handler
    return wrapper
