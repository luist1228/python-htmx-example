from contextlib import asynccontextmanager
from typing import Annotated, Any, Union
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from sqlmodel import  select, func

from src.core.db import create_db_and_tables
from src.api.main import api_router
from src.models import Todo, TodoCreate, TodoPublic, TodosPublic
from src.client.main import client_router

api_version="/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="./src/static"), name="static")

# Add Client Router for HTMX/Client operation
app.include_router(client_router)


# Separate API routes from base path
api = FastAPI()
api.include_router(api_router, prefix=api_version)

app.mount("/api", api)
