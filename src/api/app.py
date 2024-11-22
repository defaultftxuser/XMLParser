from fastapi import FastAPI

from src.api.lifespan import run_migrations
from src.api.routers.routers.xml_handlers import router as api_router


def get_app():
    app = FastAPI(
        title="API",
        description="API for parsing xml and generating summary with gpt",
    )
    app.include_router(api_router)

    @app.on_event("startup")
    async def on_startup():
        await run_migrations()

    @app.get("/")
    async def healtcheck() -> dict[str, bool]:
        return {"Success": True}

    return app
