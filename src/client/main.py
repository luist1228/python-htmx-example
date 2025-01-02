import sys
from typing import Annotated, Union
from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import HTMLResponse

from src import utils
from .deps import ClientDep
from src.utils import themes
from .routes import todos_client 


client_router = APIRouter()

@client_router.get("/", response_class=HTMLResponse)
def base_page(request: Request,clientDep:ClientDep):
    with open(utils.CONTENT_DIR+"home.html", 'r') as f:
        html_as_string= f.read()
    return clientDep.htmx_template_response(
        name="pages/home.html",
        request=request, 
        
        context= {
            "title" : "Python + HTMX",
            "themes" : themes,
            "readme":html_as_string
        }
    )

client_router.include_router(todos_client.router)
