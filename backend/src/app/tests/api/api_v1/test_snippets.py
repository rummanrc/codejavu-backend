import pytest

# from fastapi.testclient import TestClient
from httpx import AsyncClient
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.snippet import create_random_snippet

pytestmark = pytest.mark.asyncio


async def test_create_snippet(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    data = {
        "title": "oldddd",
        "snippet": "<?php echo \"heyy\">",
        "language_id": {
            "id": 1
        },
        "links": [
            {"url": "new_url2"}
        ],
        "tags": [
            {
                "id": 1,
                "name": "bla"
            }
        ]
    }
    response = await client.post(
        f"{settings.API_V1_STR}/snippets/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "user_id" in content


async def test_read_snippet(
        client: AsyncClient, superuser_token_headers: dict, async_get_db: AsyncSession
) -> None:
    snippet = await create_random_snippet(async_get_db)
    response = await client.get(
        f"{settings.API_V1_STR}/snippets/{snippet.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == snippet.title
    assert content["description"] == snippet.description
    assert content["id"] == snippet.id
    assert content["user_id"] == snippet.user_id