from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.services import playlist_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/context-menu")
def get_context_menu(filepath: str):
    playlists = playlist_service.list_playlists()
    html = '<div class="text-muted small mb-2 px-2">Ajouter à la playlist :</div>'

    for playlist in playlists:
        html += f'''
        <div class="context-menu-item text-white" 
             hx-post="/playlists/{playlist}/add" 
             hx-vals='{{"filepath": "{filepath}"}}'
             hx-trigger="click"
             hx-on:htmx:after-request="
                document.getElementById('trackContextMenu').classList.add('d-none'); 
                if(event.detail.successful) {{
                    showToast('Ajouté à {playlist}', 'success');
                }} else {{
                    showToast('Erreur lors de l\\'ajout à {playlist}', 'danger');
                }}
             ">
            📁 {playlist}
        </div>
        '''

    html += '''
    <hr class="text-secondary my-2">
    <div class="context-menu-item text-primary" 
         onclick="document.getElementById('trackContextMenu').classList.add('d-none')"
         data-bs-toggle="modal" 
         data-bs-target="#createPlaylistModal">
        ➕ Nouvelle playlist...
    </div>
    '''
    return HTMLResponse(html)