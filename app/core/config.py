from pathlib import Path

# Racine du projet
BASE_DIR = Path("/home/collinm")

# Dossier contenant les fichiers audio
AUDIO_DIR = BASE_DIR / "Music"

# Dossier où seront stockées les playlists
PLAYLISTS_DIR = BASE_DIR / ".echoNest" / "playlists"
PLAYLISTS_DIR.mkdir(parents=True, exist_ok=True)

HISTORICAL_TRACKS_DIR = BASE_DIR / ".echoNest" / "historical_tracks"
HISTORICAL_TRACKS_DIR.mkdir(parents=True, exist_ok=True)

# Extensions audio autorisées
ALLOWED_AUDIO_EXTENSIONS = [".mp3", ".wav", ".flac", ".ogg"]

# Paramètres serveur
SERVER_NAME = "EchoNest"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

# Debug mode
DEBUG = True

# Static & templates (pour Bootstrap + lecteur web)
TEMPLATE_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"

# Access token pour la librairie genius
GENIUS_ACCESS_TOKEN = "vzJQWF7v1hg-izK0PhUfAd6SAsbtuzZQlJxL0ar1_vJ-VlNFdas9tTrHTuYFci_s"