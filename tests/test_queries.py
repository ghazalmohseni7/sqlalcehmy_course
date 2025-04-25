import random
import pytest
import sqlalchemy as sqla
from faker import Faker
from models import *

fake = Faker()


class TestInsert:
    @pytest.mark.asyncio
    async def test_insert_category(self, async_session1):
        print(1111111111111111111111111111, type(async_session1))
        import asyncio
        loop = asyncio.get_event_loop()
        print(
            f"***************************************************Event Loop ID (Fixture test_insert_category): {id(loop)}")

        new_cat = Category(name=fake.word())
        async_session1.add(new_cat)
        await async_session1.commit()
        await async_session1.refresh(new_cat)

        assert new_cat.id is not None
