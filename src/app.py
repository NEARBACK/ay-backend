from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette_context.middleware import RawContextMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from api.router import api_router
from core.exceptions import register_exception_handlers
from core.lifespan import lifespan
from core.middlewares import LogRequestIdMiddleware
from core.settings import settings

app = FastAPI(
    title=settings.app_title,
    root_path=settings.root_path,
    redoc_url=None,
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

app.add_middleware(LogRequestIdMiddleware)
app.add_middleware(RawContextMiddleware)
app.add_middleware(
    PrometheusMiddleware,
    app_name=settings.app_title,
    group_paths=True,
    filter_unhandled_paths=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router, prefix="/api")

app.add_route("/metrics", handle_metrics)

register_exception_handlers(app)
