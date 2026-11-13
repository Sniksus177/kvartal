from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from data.users import create_user, get_user_by_email, get_user_by_id, check_user_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    if current_user(request):
        return RedirectResponse("/profile", status_code=303)
    error = request.session.pop("user_error", "")
    return templates.TemplateResponse(
        request=request, name="register.html", context={"error": error}
    )


@router.post("/register")
async def register(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
    password_repeat: str = Form("")
):
    name = name.strip()
    email = email.strip().lower()

    if len(name) < 2:
        error = "Введите имя (не меньше двух символов)."
    elif "@" not in email or "." not in email.split("@")[-1]:
        error = "Введите правильный адрес электронной почты."
    elif len(password) < 8:
        error = "Пароль должен содержать не менее 8 символов."
    elif password != password_repeat:
        error = "Пароли не совпадают."
    elif get_user_by_email(email):
        error = "Пользователь с такой почтой уже зарегистрирован."
    else:
        user_id = create_user(name, email, password)
        if user_id:
            request.session.clear()
            request.session["user_id"] = user_id
            return RedirectResponse("/profile", status_code=303)
        error = "Не удалось создать аккаунт. Попробуйте ещё раз."

    request.session["user_error"] = error
    return RedirectResponse("/register", status_code=303)


@router.get("/user/login", response_class=HTMLResponse)
async def user_login_page(request: Request):
    if current_user(request):
        return RedirectResponse("/profile", status_code=303)
    error = request.session.pop("user_error", "")
    return templates.TemplateResponse(
        request=request, name="user_login.html", context={"error": error}
    )


@router.post("/user/login")
async def user_login(
    request: Request,
    email: str = Form(""),
    password: str = Form("")
):
    email = email.strip().lower()
    user = get_user_by_email(email)

    if check_user_password(user, password):
        request.session.clear()
        request.session["user_id"] = user["id"]
        return RedirectResponse("/profile", status_code=303)

    request.session["user_error"] = "Неверная почта или пароль."
    return RedirectResponse("/user/login", status_code=303)


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/user/login", status_code=303)

    return templates.TemplateResponse(
        request=request, name="profile.html", context={"user": user}
    )


@router.get("/user/logout")
async def user_logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse("/", status_code=303)
