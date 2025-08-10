import logging
import lyricsgenius
import re

from app.core.config import GENIUS_ACCESS_TOKEN

logger = logging.getLogger(__name__)

# Initialisation unique de l'instance Genius
genius = lyricsgenius.Genius(
    access_token=GENIUS_ACCESS_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
    verbose=False,  # Désactivé car on gère les logs nous-mêmes
    timeout=15
)

# Cache simple en mémoire (reset au redémarrage)
_lyrics_cache = {}

def search_song_lyrics(title: str, artist: str) -> dict | None:

    if not title or not artist:
        logger.warning("Titre ou artiste manquant")
        return None

    # Normalisation pour le cache
    cache_key = f"{artist.lower().strip()}::{title.lower().strip()}"

    # 1. Vérifie le cache (seulement les succès)
    if cache_key in _lyrics_cache:
        logger.info(f"🎵 Cache hit pour : {title} – {artist}")
        return _lyrics_cache[cache_key]

    try:
        logger.info(f"🔍 Recherche sur Genius : {title} – {artist}")
        song = genius.search_song(title, artist)

        if song and song.lyrics:
            # Nettoyage des paroles
            cleaned_lyrics = song.lyrics

            # Enlève tout avant "Lyrics"
            if "Lyrics" in cleaned_lyrics:
                cleaned_lyrics = cleaned_lyrics.split("Lyrics", 1)[1]

            # Enlève la partie "Embed" à la fin
            if "Embed" in cleaned_lyrics:
                cleaned_lyrics = cleaned_lyrics.split("Embed", 1)[0].strip()

            # Nettoie les espaces multiples
            cleaned_lyrics = "\n".join(line.strip() for line in cleaned_lyrics.splitlines() if line.strip())

            result = {
                "title": song.title,
                "artist": song.artist,
                "lyrics": cleaned_lyrics,
                "year": extract_year(song.album.get("release_date_for_display") if song.album else None),
                "album": song.album.get('full_title') or "Inconnu",
                "album_art": song.song_art_image_url,
                "header_image": song.header_image_url,
                "source": "Genius"
            }

            # Mise en cache uniquement en cas de succès
            _lyrics_cache[cache_key] = result
            logger.info(f"Paroles trouvées : {title} – {artist}")
            return result

        else:
            logger.info(f"Paroles non trouvées sur Genius : {title} – {artist}")
            return None

    except Exception as e:
        logger.error(f"Erreur lors de la recherche sur Genius: {e}", exc_info=True)
        return None

def extract_year(release_str):
    if not release_str:
        return "Inconnu"
    match = re.search(r'\b(19|20)\d{2}\b', release_str)
    return match.group(0) if match else "Inconnu"