from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.library_service import get_library

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# API JSON : /api/library
@router.get("/api/library")
def get_library_json(
        search: str = Query(None),
        title: str = Query(None),
        artist: str = Query(None),
        album: str = Query(None),
        genre: str = Query(None),
        year: str = Query(None)
):
    tracks = get_library(search, title, artist, album, genre, year)
    return {"tracks": tracks}

# Page HTML principale : /library
@router.get("/library", response_class=HTMLResponse)
def library_page(request: Request):
    # mais on rend un template PARTIEL qui contient juste le contenu principal
    return templates.TemplateResponse("partials/library_content.html", {"request": request})

#Grille partielle pour HTMX : /library/search
@router.get("/library/search", response_class=HTMLResponse)
def library_grid(
        request: Request,
        search: str = Query(None),
        title: str = Query(None),
        artist: str = Query(None),
        album: str = Query(None),
        genre: str = Query(None),
        year: str = Query(None),
):
    tracks = get_library(search, title, artist, album, genre, year)
    return templates.TemplateResponse("partials/library_table.html", {"request": request, "tracks": tracks})

