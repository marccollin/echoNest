from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.services import playlist_service, library_service

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

class PlaylistCreate(BaseModel):
    name: str

@router.post("/playlists", response_class=HTMLResponse)
def create_playlist(request: Request, name: str = Form(...)):
    playlist_service.create_playlist(name)
    playlists = playlist_service.list_playlists()
    return templates.TemplateResponse("partials/playlist_links.html", {"request": request, "playlists": playlists})

# Retourne la list des playlist
@router.get("/api/playlists")
def list_playlists(request: Request):
    playlists = playlist_service.list_playlists()
    return {"playlists": playlists}

@router.get("/playlists", response_class=HTMLResponse)
def list_playlists(request: Request):
    playlists = playlist_service.list_playlists()
    return templates.TemplateResponse("partials/playlist_links.html", {"request": request, "playlists": playlists})


@router.get("/playlists/{playlist_name}", response_class=HTMLResponse)
def view_playlist(request: Request, playlist_name: str):
    playlist_filepaths = playlist_service.get_playlist(playlist_name)  # liste de chemins

    all_tracks = library_service.get_library()  # récupère la bibliothèque complète

    tracks = [track for track in all_tracks if track["filepath"] in playlist_filepaths]

    if request.headers.get("HX-Request"):
        # Requête HTMX → injecte juste la section centrale
        return templates.TemplateResponse("partials/playlist_tracks.html", {
            "request": request,
            "playlist_name": playlist_name,
            "tracks": tracks
        })
    else:
        # Requête normale → page complète
        return templates.TemplateResponse("playlist.html", {
            "request": request,
            "name": playlist_name,
            "tracks": tracks
        })

@router.delete("/playlists/{playlist_name}", response_class=HTMLResponse)
def delete_playlist(playlist_name: str, request: Request):
    playlist_service.remove_playlist(playlist_name)
    playlists = playlist_service.list_playlists()
    return templates.TemplateResponse("partials/playlist_links.html", {"request": request, "playlists": playlists})

@router.post("/playlists/{playlist_name}/add")
def add_track(playlist_name: str, filepath: str = Form()):
    return playlist_service.add_track_to_playlist(playlist_name, filepath)

@router.delete("/playlists/{playlist_name}/track")
def remove_track(playlist_name: str, filepath: str = Query(..., description="Chemin relatif du fichier à supprimer")):
    return playlist_service.remove_track_from_playlist(playlist_name, filepath)
