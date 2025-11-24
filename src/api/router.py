from fastapi.routing import APIRouter

from api.api_v1 import dummy
from api.api_v1.infra.handlers import infra_router

api_router = APIRouter()
api_router.include_router(dummy.router, prefix="/dummy", tags=["Dummy"])
api_router.include_router(infra_router, prefix="/infra", tags=["Infra"])
