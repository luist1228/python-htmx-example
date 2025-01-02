from typing import Annotated, Any, Mapping, Union
from fastapi import Depends, Header, Request
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask
from src.utils import themes

templates = Jinja2Templates(directory="./src/templates")

# Get Htmx request header and check if request is made with HTMX
async def get_htmx_header(hx_request: Union[str, None] = Header(default=None)):
    if hx_request :
        return True
    return False


# Dependencie for HTMX request header and Template response
class ClientDependencies:
    def __init__(self, hx_request: Union[str, None] = Header(default=None)) -> None:
        self.templates = templates
        self.isHtmx = False
        if hx_request :
            self.isHtmx=True
    
    # Custom template response with htmx header added to the response context
    def htmx_template_response(
        self, 
        request: Request,
        name: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None
    ):  
        baseContext = {
            "isHtmx":self.isHtmx,
            "themes": themes,
        }
        if context is not None:
            context = {
                **baseContext,
                **context
            }
        else:
            context = {
                **baseContext,
            } 
        return self.templates.TemplateResponse(
            name=name, 
            request=request,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            context=context,
            background=background
        )
        
ClientDep = Annotated[ClientDependencies, Depends(ClientDependencies)]
    