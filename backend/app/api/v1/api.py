from fastapi import APIRouter
from app.api.v1.routes import health, auth, analysis, decisions, dashboard

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(analysis.router)
api_router.include_router(decisions.router)
api_router.include_router(dashboard.router)
