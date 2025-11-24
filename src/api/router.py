from fastapi.routing import APIRouter

from api.api_v1 import donation, dummy, post, user
from api.api_v1.infra.handlers import infra_router

api_router = APIRouter()
api_router.include_router(dummy.router, prefix="/dummy", tags=["Dummy"])
api_router.include_router(infra_router, prefix="/infra", tags=["Infra"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(post.router, prefix="/post", tags=["Post"])
api_router.include_router(donation.router, prefix="/donation", tags=["Donation"])
