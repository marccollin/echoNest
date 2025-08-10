from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import routes_library, routes_playlist, routes_stream, routes_track, routes_ui, routes_historical  ##, routes_search, routes_playlist

app = FastAPI(title="EchoNest")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Inclusion des routes
app.include_router(routes_library.router, tags=["library"])
app.include_router(routes_playlist.router, tags=["playlist"])
app.include_router(routes_stream.router, tags=["stream"])
app.include_router(routes_track.router, tags=["track"])
app.include_router(routes_ui.router, tags=["ui"])

app.include_router(routes_historical.router, tags=["historical"])