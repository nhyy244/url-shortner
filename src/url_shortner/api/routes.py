import random
import string

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from src.url_shortner.db.connection import get_pool
from src.url_shortner.db import queries

router = APIRouter()


@router.post("/generate")
async def generate(original_url: HttpUrl) -> str:
    pool = await get_pool()
    existing_url_id = await queries.get_url_id(pool, str(original_url))
    if existing_url_id:
        return existing_url_id

    url_id: str = _generate_id()

    await queries.insert_mapping(pool, url_id, str(original_url))
    return url_id


@router.get("/{url_id}")
async def redirect(url_id: str) -> RedirectResponse:
    pool = await get_pool()
    original_url = await queries.get_original_url(pool, url_id)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=original_url, status_code=302)


def _generate_id() -> str:
    ID_LENGTH = 8
    characters = string.ascii_letters + string.digits  # base62
    return "".join(random.choice(characters) for _ in range(ID_LENGTH))
