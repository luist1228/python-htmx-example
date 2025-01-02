from contextlib import asynccontextmanager
from typing import Annotated, Any, Union
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
import markdown
from sqlmodel import  Session, select, func
from src import utils
from src.core.db import create_db_and_tables, engine
from src.api.main import api_router
from src.models import Todo, TodoCreate, TodoPublic, TodosPublic
from src.client.main import client_router
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware


api_version="/v1"



@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        create_db_and_tables(session)
    utils.generate_content_files()
    yield
    

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="./src/static"), name="static")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(GZipMiddleware)

# Add Client Router for HTMX/Client operation
app.include_router(client_router)

# Separate API routes from base path
api = FastAPI()
api.include_router(api_router, prefix=api_version)

app.mount("/api", api)
