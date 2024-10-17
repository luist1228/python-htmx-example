from typing import Annotated
from fastapi import Depends
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="./src/templates")

def get_templates() :
    yield templates

TemplateDep = Annotated[Jinja2Templates, Depends(get_templates)]  