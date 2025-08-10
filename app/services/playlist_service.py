import json
from pathlib import Path
from typing import List

from fastapi import HTTPException

from app.core.config import AUDIO_DIR, PLAYLISTS_DIR

def get_playlist_path(playlist_name: str) -> Path:
    return PLAYLISTS_DIR / f"{playlist_name}.json"

def create_playlist(name: str):
    path = get_playlist_path(name)

    if not str(path.resolve()).startswith(str(PLAYLISTS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid playlist path.")

    if path.exists():
        raise HTTPException(status_code=400, detail="Playlist already exists.")
    with open(path, "w") as f:
        json.dump([], f)
    return {"message": f"Playlist '{name}' created."}

def list_playlists() -> List[str]:
    return [p.stem for p in PLAYLISTS_DIR.glob("*.json")]

def get_playlist(name: str) -> List[str]:
    path = get_playlist_path(name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found.")
    with open(path, "r") as f:
        return json.load(f)

def add_track_to_playlist(name: str, filepath: str):
    path = get_playlist_path(name)

    if not str(path.resolve()).startswith(str(PLAYLISTS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid playlist path.")

    full_track_path = AUDIO_DIR / filepath

    if not path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found.")

    if not full_track_path.exists():
        raise HTTPException(status_code=404, detail="Track not found.")

    with open(path, "r") as f:
        playlist = json.load(f)

    if filepath in playlist:
        raise HTTPException(status_code=400, detail="Track already in playlist.")

    playlist.append(filepath)

    with open(path, "w") as f:
        json.dump(playlist, f, indent=2)

    return {"message": "Track added to playlist."}


def remove_track_from_playlist(name: str, filepath: str):
    path = get_playlist_path(name)

    if not path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found.")

    # Vérifier que le chemin est bien dans le répertoire autorisé
    if not str(path.resolve()).startswith(str(PLAYLISTS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid playlist path.")

    try:
        with open(path, "r", encoding="utf-8") as f:
            playlist = json.load(f)

        # S'assurer que la playlist est bien une liste
        if not isinstance(playlist, list):
            raise HTTPException(status_code=500, detail="Invalid playlist format: expected a list.")

        if filepath not in playlist:
            raise HTTPException(status_code=404, detail="Track not in playlist.")

        playlist.remove(filepath)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(playlist, f, indent=2, ensure_ascii=False)

        return {"message": "Track removed from playlist."}

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in playlist file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the playlist.")

def remove_playlist(playlist_name):
    path = get_playlist_path(playlist_name)

    # securité: s'assure que le path est dans PLAYLISTS_DIR
    if not str(path.resolve()).startswith(str(PLAYLISTS_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid playlist path.")

    if not path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found.")

    try:
        path.unlink()  # suppresion du fichier
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete playlist: {str(e)}")

    return {"message": f"Playlist '{playlist_name}' deleted."}


def get_tracks(playlist_name):
    path = get_playlist_path(playlist_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Playlist not found")
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
