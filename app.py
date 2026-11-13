from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from config import Config
from routes import register_routes
from data.users import init_users


def create_app():
    app = FastAPI()
    app.add_middleware(
        SessionMiddleware,
        secret_key=Config.SECRET_KEY,
        same_site="lax",
        https_only=False
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")
    init_users()
    register_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
