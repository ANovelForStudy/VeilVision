import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from src.config import application_config


async def lifespan(app: FastAPI):
    yield


def main():
    app = FastAPI(
        lifespan=lifespan,
        # ! TODO: Move to .env
        debug=True,
    )

    uvicorn.run(
        app,
    )


if __name__ == "__main__":
    main()
