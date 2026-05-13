import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent.parent),
)

from typing import Type

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import include_routers
from src.config import Config
from src.config.base import BaseConfig
from src.config.database import PostgresSettings
from src.dependencies.providers import get_all_providers


def get_fastapi_application() -> FastAPI:
    # ! TODO: Replace with Offline docs
    app = FastAPI(
        # ! TODO: Move to .env
        debug=True,
        redirect_slashes=True,
    )

    configure_dishka_container(app)

    app.add_middleware(
        CORSMiddleware,
        # ! TODO: Replace with specific values
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_routers(app)

    return app


def configure_dishka_container(
    app: FastAPI,
    config: Config | None = None,
) -> None:
    if config is None:
        config = Config()

    context: dict[Type[BaseConfig], BaseConfig] = {
        PostgresSettings: config.postgres_settings,
    }

    dependency_container = make_async_container(
        *get_all_providers(),
        context=context,
    )

    setup_dishka(
        container=dependency_container,
        app=app,
    )


def main():
    uvicorn.run(
        "src.main:get_fastapi_application",
        # ! TODO: Move to .env
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
