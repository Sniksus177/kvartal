from routes.pages import router as pages_router
from routes.applications import router as applications_router
from routes.auth import router as auth_router
from routes.users import router as users_router


def register_routes(app):
    app.include_router(pages_router)
    app.include_router(applications_router)
    app.include_router(auth_router)
    app.include_router(users_router)
