from asyncpg import Pool


async def get_url_id(pool: Pool, original_url: str) -> str | None:
    row = await pool.fetchrow(
        "SELECT url_id FROM urls WHERE original_url = $1",
        original_url,
    )
    return row["url_id"] if row else None


async def get_original_url(pool: Pool, url_id: str) -> str | None:
    row = await pool.fetchrow(
        "SELECT original_url FROM urls WHERE url_id = $1",
        url_id,
    )
    return row["original_url"] if row else None


async def insert_mapping(pool: Pool, url_id: str, original_url: str) -> None:
    await pool.execute(
        "INSERT INTO urls (url_id, original_url) VALUES ($1, $2)",
        url_id,
        original_url,
    )
