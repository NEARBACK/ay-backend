import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette_context import context

from src.core.logger import SM_LOG_ID, RequestContext, RequestContextKey


class LogRequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        sm_log_id = request.headers.get(SM_LOG_ID, f"{uuid.uuid4().hex}-unknown")
        context[SM_LOG_ID] = sm_log_id

        context[RequestContextKey] = RequestContext(
            request_id=uuid.uuid4().hex, method=request.method, path=request.url.path
        )

        response: Response = await call_next(request)
        context[RequestContextKey].status_code = response.status_code
        response.headers[SM_LOG_ID] = context[SM_LOG_ID]
        return response
