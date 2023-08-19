import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import LanguageCreate
from app.schemas.link import LinkCreate
from app.schemas.snippet import SnippetCreate, SnippetUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.snippet import initialize_data
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_snippet(async_get_db: AsyncSession) -> None:
    save_data = await save_snippet(async_get_db)
    snippet = save_data['snippet']
    assert snippet.title == save_data['title']
    assert snippet.snippet == save_data['snippet_text']
    assert snippet.language.name == save_data['language_name']
    assert snippet.links[0].url == save_data['link_url']
    assert snippet.tags[0].id == 1  # todo get rid of magic number
    assert snippet.user_id == save_data['user_id']


async def test_get_snippet(async_get_db: AsyncSession) -> None:
    save_data = await save_snippet(async_get_db)
    snippet = save_data['snippet']
    stored_snippet = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert stored_snippet
    assert snippet.id == stored_snippet.id
    assert snippet.title == stored_snippet.title
    assert snippet.snippet == stored_snippet.snippet
    assert snippet.language.name == save_data['language_name']
    assert snippet.user_id == stored_snippet.user_id
    assert snippet.links == stored_snippet.links
    assert snippet.tags == stored_snippet.tags


async def test_update_snippet(async_get_db: AsyncSession) -> None:
    save_data = await save_snippet(async_get_db)
    snippet = save_data['snippet']
    snippet_text2 = "updated snippet"
    snippet_update = SnippetUpdate(snippet=snippet_text2)

    snippet2 = await crud.snippet.update(db=async_get_db, db_obj=snippet, obj_in=snippet_update)
    assert snippet.id == snippet2.id
    assert snippet.title == snippet2.title
    assert snippet2.snippet == snippet_text2
    assert snippet.user_id == snippet2.user_id


async def test_delete_snippet(async_get_db: AsyncSession) -> None:
    save_data = await save_snippet(async_get_db)
    snippet = save_data['snippet']
    snippet2 = await crud.snippet.remove(db=async_get_db, id=snippet.id)
    snippet3 = await crud.snippet.get(db=async_get_db, id=snippet.id)
    assert snippet3 is None
    assert snippet2.id == snippet.id
    assert snippet2.title == save_data['title']
    assert snippet2.snippet == save_data['snippet_text']
    assert snippet2.user_id == save_data['user_id']


async def save_snippet(async_get_db: AsyncSession) -> dict:
    user = await create_random_user(async_get_db)
    await initialize_data(async_get_db, user_id=user.id) # todo receive data from here
    title = random_lower_string()
    snippet_text = random_lower_string()
    language = LanguageCreate(id=1, name="Java")
    link = LinkCreate(url="https://snip.pet")
    snippet_in = SnippetCreate(title=title, snippet=snippet_text, language_id=1, tag_ids=[1], links=[link])
    snippet = await crud.snippet.create_with_owner(db=async_get_db, obj_in=snippet_in, user_id=user.id)

    return {
        'user_id': user.id,
        'title': title,
        'language_name': language.name,
        'link_url': link.url,
        'snippet_text': snippet_text,
        'snippet': snippet,
    }