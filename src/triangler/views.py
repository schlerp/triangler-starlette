from starlette.requests import Request
from starlette.responses import HTMLResponse

from triangler.templating import template


async def home_page(request: Request) -> HTMLResponse:
    return template.TemplateResponse("home.html.jinja", context={"request": request})
