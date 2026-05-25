from asyncpg import Pool

_MIGRATIONS: list[str] = [
    """
    CREATE TABLE IF NOT EXISTS urls (
        url_id       TEXT        PRIMARY KEY,
        original_url TEXT        NOT NULL UNIQUE,
        created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_urls_original ON urls (original_url)
    """,
]


async def run_migrations(pool: Pool) -> None:
    for sql in _MIGRATIONS:
        await pool.execute(sql)
