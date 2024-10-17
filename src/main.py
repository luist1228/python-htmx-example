from contextlib import asynccontextmanager
from typing import Annotated, Any, Union
from fastapi import FastAPI, Query
from sqlmodel import  select, func

from src.core.db import create_db_and_tables
from src.api.main import api_router
from src.models import Todo, TodoCreate, TodoPublic, TodosPublic

api_version="/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)

# Separate API routes from base path
api = FastAPI()
api.include_router(api_router, prefix=api_version)

app.mount("/api", api)
