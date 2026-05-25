import random
import string
from typing import TypedDict

import asyncpg
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from url_shortner.db.connection import get_pool
from url_shortner.db import queries

router = APIRouter()


class GenerateResponse(TypedDict):
    url_id: str
    collisions: int


@router.post("/generate")
async def generate(original_url: HttpUrl) -> GenerateResponse:
    pool = await get_pool()
    existing_url_id = await queries.get_url_id(pool, str(original_url))
    if existing_url_id:
        return GenerateResponse(url_id=existing_url_id, collisions=0)

    collisions = 0
    while True:
        url_id = _generate_id()
        try:
            await queries.insert_mapping(pool, url_id, str(original_url))
            return GenerateResponse(url_id=url_id, collisions=collisions)
        except asyncpg.UniqueViolationError:
            collisions += 1


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
