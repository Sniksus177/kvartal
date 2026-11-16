from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from routes.users import current_user
router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    messages = request.session.pop("_flashes", [])
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"messages": messages, "user": current_user(request)},
    )
