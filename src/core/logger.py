import logging
from dataclasses import dataclass

from starlette_context import context

from core.settings import settings

RequestContextKey = "RequestContextKey"
SM_LOG_ID = "Sm-Log-ID"  # идентификатор на уровне системы (cквозное логирование)


def get_request_context() -> "RequestContext":
    if context.exists():
        return context.get(RequestContextKey, RequestContext())
    return RequestContext()


@dataclass
class RequestContext:
    request_id: str = ""  # идентификатор на уровне приложения
    method: str = ""
    path: str = ""
    status_code: int | None = None

    def clear(self) -> None:
        self.request_id = "system"
        self.method = ""
        self.path = ""
        self.status_code = None


SERVICE_LOG_FORMAT = "[%(levelname)s][%(method)s][%(path)s][%(request_id)s] - %(message)s"
UVICORN_LOG_FORMAT = "[%(levelname)s][%(method)s][%(path)s][%(request_id)s] - Status: %(status_code)s"


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        request_context = get_request_context()
        record.request_id = request_context.request_id
        record.method = request_context.method
        record.path = request_context.path
        record.status_code = request_context.status_code
        return True


def configure_logger(
    logger_name: str,
    log_format: str,
    log_level: int = logging.INFO,
) -> None:
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))

    logger.propagate = False
    logger.addHandler(handler)
    logger.addFilter(RequestIdFilter())
    logger.setLevel(log_level)


service_logger_log_level = logging.DEBUG if settings.debug else logging.INFO
configure_logger("service_logger", SERVICE_LOG_FORMAT, service_logger_log_level)
configure_logger("uvicorn.access", UVICORN_LOG_FORMAT)

service_logger = logging.getLogger("service_logger")
