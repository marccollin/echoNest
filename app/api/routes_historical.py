from fastapi import APIRouter, Request
from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

from app.services.historical_service import load_historical_tracks, add_track_to_historical, get_historical_stats, remove_track_from_historical, clear_historical_file

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

class RemoveTrackRequest(BaseModel):
    filepath: str

@router.post("/historical/clear")
def clear_historical(request: Request):
    # Vider l'historique
    clear_historical_file()

    # Recharger les pistes (maintenant vides)
    tracks = load_historical_tracks()  # → liste vide

    # Récupérer les stats (seront toutes à zéro)
    stats = get_historical_stats()

    # Renvoyer le template HTML mis à jour
    return templates.TemplateResponse(
        "partials/historical.html",
        {"request": request, "tracks": tracks, "stats": stats}
    )


@router.get("/historical")
def get_historical_page(request: Request):
    historical_tracks = load_historical_tracks()

    stats = get_historical_stats()

    return templates.TemplateResponse(
        "partials/historical.html",
        {"request": request, "tracks": historical_tracks, "stats": stats}
    )

@router.post("/api/historical/add")
def add_to_historical(data: dict):
    filepath = data.get("filepath")
    if filepath:
        add_track_to_historical(filepath)
        # Retourner les nouvelles stats
        stats = get_historical_stats()
        return {"status": "ok", "stats": stats}
    return {"status": "error"}