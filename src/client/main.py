from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .deps import TemplateDep
from src.utils import themes


client_router = APIRouter()

@client_router.get("/", response_class=HTMLResponse)
def home_page(request: Request, templates: TemplateDep):
  return templates.TemplateResponse(
        request=request, 
        name="main_layout.html",
        context= {
            "title" : "Python + HTMX",
            "themes" : themes
        }
    )

