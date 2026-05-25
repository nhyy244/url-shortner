from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.url_shortner.db.connection import close_pool, init_pool
from src.url_shortner.db.migrations import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    pool = await init_pool()
    await run_migrations(pool)
    try:
        yield
    finally:
        await close_pool()
