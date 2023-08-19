from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas
from app.schemas.link import LinkCreate
from app.schemas.snippet import SnippetCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_snippet(db: AsyncSession, *, user_id: Optional[int] = None) -> models.Snippet:
    if user_id is None:
        user = await create_random_user(db)
        user_id = user.id
    await initialize_data(db, user_id)
    title = random_lower_string()
    description = random_lower_string()
    link = LinkCreate(url="https://snip.pet")
    snippet_in = SnippetCreate(title=title, snippet=description, language_id=1, tag_ids=[1], links=[link])
    return await crud.snippet.create_with_owner(db=db, obj_in=snippet_in, user_id=user_id)


async def initialize_data(db: AsyncSession, user_id: Optional[int] = None):
    languages = [
        {"id": 1, "name": "Java"},
        {"id": 2, "name": "Python"},
    ]
    tags = [
        {"id": 1, "name": "Red"},
        {"id": 2, "name": "Blue"},
    ]
    for language in languages:
        language_in = schemas.LanguageCreate(name=language["name"])
        language = await crud.language.create(db, obj_in=language_in)  # noqa: F841
    for tag in tags:
        tag_in = schemas.TagCreate(name=tag["name"])
        tag = await crud.tag.create_with_owner(db, obj_in=tag_in, user_id=user_id)  # noqa: F841