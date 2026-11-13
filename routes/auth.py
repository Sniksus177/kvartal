from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from config import Config, check_admin_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("admin"):
        return RedirectResponse("/admin", status_code=303)

    error = request.session.pop("login_error", "")
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error}
    )


@router.post("/login")
async def login(request: Request, username: str = Form(""), password: str = Form("")):
    username = username.strip()

    if username == Config.ADMIN_LOGIN and check_admin_password(password):
        request.session.clear()
        request.session["admin"] = True
        return RedirectResponse("/admin", status_code=303)

    request.session["login_error"] = "Неверный логин или пароль."
    return RedirectResponse("/login", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
