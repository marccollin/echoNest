import os
import re
from pathlib import Path
import threading
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

from app.core.config import AUDIO_DIR, SERVER_HOST, SERVER_PORT

BASE_STREAM_URL = SERVER_HOST + ":" + str(SERVER_PORT) + "/stream"

# Cache global
_library_cache = []
_cache_lock = threading.Lock()
_cache_initialized = False

def _initialize_library_cache():
    #Scan le répertoire et remplit le cache (une seule fois)
    global _library_cache, _cache_initialized

    if _cache_initialized:
        return

    with _cache_lock:
        if _cache_initialized:  # double-check
            return

        tracks = []
        audio_dir = Path(AUDIO_DIR)

        for root, _, files in os.walk(audio_dir):
            for file in files:
                if not file.lower().endswith((".mp3", ".wav", ".flac")):
                    continue

                full_path = Path(root) / file
                rel_path = full_path.relative_to(audio_dir)

                try:
                    if file.lower().endswith(".mp3"):
                        audio = MP3(full_path, ID3=EasyID3)
                        meta_title = audio.get("title", [None])[0]
                        meta_artist = audio.get("artist", [None])[0]
                        meta_album = audio.get("album", [None])[0]
                        meta_genre = audio.get("genre", [None])[0]
                        meta_year = extract_year(audio)
                        meta_duration = int(audio.info.length)
                    else:
                        # Gérer WAV/FLAC
                        meta_title = meta_artist = meta_album = meta_genre = meta_year = None
                        meta_duration = 0
                except Exception as e:
                    print(f"Erreur lecture {file}: {e}")
                    meta_title = meta_artist = meta_album = meta_genre = meta_year = ""
                    meta_duration = 0

                tracks.append({
                    "filename": file,
                    "filepath": str(rel_path.as_posix()),
                    "title": meta_title or "",
                    "artist": meta_artist or "",
                    "album": meta_album or "",
                    "genre": meta_genre or "",
                    "year": meta_year or "",
                    "duration": meta_duration,
                    "duration_str": format_duration(meta_duration),
                    "stream_url": f"{BASE_STREAM_URL}/{rel_path.as_posix()}"
                })

        _library_cache = tracks
        _cache_initialized = True

def matches_regex(value: str, pattern: str) -> bool:
    if not isinstance(value, str):
        value = ""
    try:
        return re.search(pattern, value, re.IGNORECASE) is not None
    except re.error:
        return False  # Regex invalide


def get_library(search: str = None,
                title: str = None,
                artist: str = None,
                album: str = None,
                genre: str = None,
                year: str = None,
                duration: int = None, ):
    _initialize_library_cache()

    results = _library_cache

    if search:
        results = [t for t in results if matches_regex(t["filename"], search) or
                   matches_regex(t["title"], search) or
                   matches_regex(t["artist"], search)]

    if title:
        results = [t for t in results if matches_regex(t["title"], title)]

    if artist:
        results = [t for t in results if matches_regex(t["artist"], artist)]

    if album:
        results = [t for t in results if matches_regex(t["album"], album)]

    if genre:
        results = [t for t in results if matches_regex(t["genre"], genre)]

    if year:
        results = [t for t in results if matches_regex(str(t["year"]), year)]

    if duration:
        results = [t for t in results if t["duration"] >= duration]

    return results


def format_duration(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

def extract_year(audio) -> str:
    for key in ["date", "year", "originaldate", "recording_date"]:
        value = audio.get(key, [None])[0]
        if value:
            return value
    return ""
