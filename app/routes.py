from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.product_router import router as product_router

api_router = APIRouter()

# Registrar cada router individual
api_router.include_router(health_router)
api_router.include_router(product_router)
# api_router.include_router(users_router) # Agrega aquí futuros routers