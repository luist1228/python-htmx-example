from fastapi import APIRouter
from .routes import todos_api as todos_routes

api_router = APIRouter()

api_router.include_router(todos_routes.router)