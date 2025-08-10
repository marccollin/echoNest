from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.services.genius_service import search_song_lyrics

router = APIRouter()

@router.get("/track/lyrics")
def get_lyrics(artist: str, title: str):
    if not artist or not title:
        return HTMLResponse('<p class="text-danger">Artiste et titre requis.</p>', status_code=400)

    song_data = search_song_lyrics(title, artist)  # Retourne un dict

    if not song_data:
        return HTMLResponse('<p class="text-muted">Paroles non trouvées.</p>')

    # Utilise les infos enrichies
    return HTMLResponse(f'''
        <div class="d-flex mb-3 align-items-center">
            <img src="{song_data["album_art"]}" width="80" class="rounded me-3">
            <div>
                <strong>{song_data["title"]}</strong><br>
                <small>{song_data["artist"]} - {song_data["album"]} -{song_data["year"]}</small><br>
                
            </div>
        </div>
        
        <pre class="lyrics-text">{song_data["lyrics"]}</pre>
                        ''')