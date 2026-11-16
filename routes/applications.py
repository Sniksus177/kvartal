from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from data.applications import add_application, get_applications

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.post("/send")
async def send_application(
        request: Request,
        name: str = Form(""),
        phone: str = Form(""),
        comment: str = Form("")
):
    name = name.strip()
    phone = phone.strip()
    comment = comment.strip()

    flashes = request.session.setdefault("_flashes", [])

    if not name or not phone:
        flashes.append("Заполните имя и номер телефона.")
    else:
        add_application(name, phone, comment)
        flashes.append("Заявка отправлена. Спасибо!")

    return RedirectResponse(url="/#contacts", status_code=303)


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"applications": get_applications()}
    )
