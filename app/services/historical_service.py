import json
import threading

from pathlib import Path
from typing import List, Dict

from app.core.config import HISTORICAL_TRACKS_DIR
from app.services.library_service import get_library

_historical_lock = threading.Lock()

def get_historical_path() -> Path:
    return HISTORICAL_TRACKS_DIR / "historic.json"


def add_track_to_historical(filepath: str, max_entries: int = 100):
    path = get_historical_path()

    with _historical_lock:
        # Lecture sécurisée
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    historical = json.load(f)
            except (json.JSONDecodeError, IOError):
                historical = []
        else:
            historical = []

        # Normaliser l'ancien format vers le nouveau
        normalized_historical = []
        for entry in historical:
            if isinstance(entry, str):
                # Convertir ancien format (string) vers nouveau format (objet)
                normalized_historical.append({
                    "filepath": entry,
                    "timestamp": None,
                    "played_at": "Historique"
                })
            else:
                # Déjà au bon format
                normalized_historical.append(entry)

        # Éviter les doublons consécutifs (comparer les filepaths)
        if (normalized_historical and
                normalized_historical[-1]["filepath"] == filepath):
            print(f"Doublon évité pour: {filepath}")
            return

        # Ajouter la nouvelle entrée avec timestamp
        from datetime import datetime
        entry = {
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        normalized_historical.append(entry)
        print(f"Ajouté à l'historique: {filepath}")

        # Limiter la taille (garder les plus récents)
        if len(normalized_historical) > max_entries:
            normalized_historical = normalized_historical[-max_entries:]

        # Écriture sécurisée
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(normalized_historical, f, indent=2, ensure_ascii=False)
            print(f"Historique sauvegardé: {len(normalized_historical)} entrées")
        except IOError as e:
            print(f"Erreur sauvegarde historique: {e}")

def load_historical_tracks() -> List[Dict]:
    """Charge l'historique et enrichit avec les métadonnées"""
    path = get_historical_path()

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            historical = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    # Enrichir avec les métadonnées de la bibliothèque
    library_tracks = {track["filepath"]: track for track in get_library()}

    enriched_tracks = []
    for entry in reversed(historical):  # Plus récent en premier
        if isinstance(entry, str):
            # Format actuel (juste le filepath)
            filepath = entry
            played_at = "Récemment"
        else:
            # Nouveau format (avec timestamp)
            filepath = entry["filepath"]
            played_at = entry.get("played_at", "Inconnu")

        # Récupérer les métadonnées
        track_info = library_tracks.get(filepath)
        if track_info:
            enriched_track = track_info.copy()
            enriched_track["played_at"] = played_at
            enriched_tracks.append(enriched_track)

    return enriched_tracks

def get_historical_stats() -> Dict:
    """Retourne des statistiques sur l'historique"""
    tracks = load_historical_tracks()

    if not tracks:
        return {"total_plays": 0, "unique_tracks": 0, "top_artist": None}

    from collections import Counter
    artists = [track["artist"] for track in tracks if track["artist"]]
    artist_counts = Counter(artists)

    return {
        "total_plays": len(tracks),
        "unique_tracks": len(set(track["filepath"] for track in tracks)),
        "top_artist": artist_counts.most_common(1)[0][0] if artist_counts else None
    }

def remove_track_from_historical(filepath: str) -> bool:
    """Retire une piste de l'historique"""
    path = get_historical_path()

    if not path.exists():
        return False

    with _historical_lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                historical = json.load(f)
        except (json.JSONDecodeError, IOError):
            return False

        # Filtrer pour retirer toutes les occurrences de ce filepath
        original_length = len(historical)
        historical = [
            entry for entry in historical
            if (entry["filepath"] if isinstance(entry, dict) else entry) != filepath
        ]

        # Vérifier si quelque chose a été supprimé
        if len(historical) == original_length:
            return False  # Aucune suppression

        # Sauvegarder le fichier modifié
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(historical, f, indent=2, ensure_ascii=False)
            print(f"Supprimé de l'historique: {filepath}")
            return True
        except IOError as e:
            print(f"Erreur suppression historique: {e}")
            return False

def clear_historical_file() -> bool:
    #Vide complètement l'historique
    path = get_historical_path()

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        print("Historique vidé")
        return True
    except IOError as e:
        print(f"Erreur vidage historique: {e}")
        return False
    #Retourne des statistiques sur l'historique
    tracks = load_historical_tracks()

    if not tracks:
        return {"total_plays": 0, "unique_tracks": 0, "top_artist": None}

    from collections import Counter
    artists = [track["artist"] for track in tracks if track["artist"]]
    artist_counts = Counter(artists)

    return {
        "total_plays": len(tracks),
        "unique_tracks": len(set(track["filepath"] for track in tracks)),
        "top_artist": artist_counts.most_common(1)[0][0] if artist_counts else None
    }