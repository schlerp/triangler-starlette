from starlette.applications import Starlette
from triangler import routes
from triangler import config
from triangler import middleware

app = Starlette(
    debug=config.DEBUG,
    routes=routes.ROUTES,
    middleware=middleware.MIDDLEWARE,
)
