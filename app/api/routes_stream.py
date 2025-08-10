import mimetypes
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import AUDIO_DIR
router = APIRouter()

@router.get("/stream/{file_path:path}")
def stream_audio(file_path: str):

    audio_path = (AUDIO_DIR / file_path).resolve()

    # S'assure que le fichier est bien dans AUDIO_DIR
    if not str(audio_path).startswith(str(AUDIO_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")

    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not audio_path.suffix.lower() in {'.mp3', '.flac', '.wav', '.ogg'}:
        raise HTTPException(status_code=415, detail="Unsupported audio format")

    # Détection du type MIME (ex: audio/mpeg, audio/flac...)
    media_type, _ = mimetypes.guess_type(str(audio_path))
    if media_type is None:
        media_type = "application/octet-stream"

    return FileResponse(
        audio_path,
        media_type=media_type,
        filename=audio_path.name
    )