import asyncpg
from asyncpg import Pool

pool: Pool | None = None

DSN = "postgresql://postgres:postgres@localhost:5432/url_shortner"


async def init_pool() -> Pool:
    global pool
    pool = await asyncpg.create_pool(DSN, min_size=2, max_size=10)
    return pool


async def close_pool() -> None:
    global pool
    if pool is not None:
        await pool.close()
        pool = None


async def get_pool() -> Pool:
    if pool is None:
        raise RuntimeError("DB pool not initialised — app startup incomplete")
    return pool
