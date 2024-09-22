from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from triangler import views

ROUTES: list[Route] = [
    Route("/", views.home_page, name="home"),
    Mount("/static", app=StaticFiles(directory="triangler/static"), name="static"),
]
