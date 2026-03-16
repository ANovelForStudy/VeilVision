import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent.parent),
)

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import api_router
from src.dependencies.container import AppProvider


def get_fastapi_application() -> FastAPI:
    app = FastAPI(
        # ! TODO: Move to .env
        debug=True,
    )

    return app


def include_routers(app: FastAPI) -> None:
    app.include_router(api_router)


def configure_dishka_container(app: FastAPI) -> None:
    container = make_async_container(
        AppProvider(),
    )

    setup_dishka(
        container=container,
        app=app,
    )


def main():
    app = get_fastapi_application()

    configure_dishka_container(app)

    include_routers(app)

    uvicorn.run(
        "src.main:get_fastapi_application",
        # ! TODO: Move to .env
        reload=True,
    )


if __name__ == "__main__":
    main()
