import random
import pytest
import sqlalchemy as sqla
from faker import Faker
from models import *

fake = Faker()


def test_a(db_session):
    assert True
class TestQueries:
    @pytest.mark.asyncio
    async def test_insert(self, db_session):
        # arrange
        category = Category(
            name=fake.word(),
        )

        async with db_session.begin():
            # act
            db_session.add(category)
            # assert
            result = await db_session.execute(
                sqla.select(Category).where(Category.name == category.name)
            )
            inserted_user = result.scalar_one_or_none()
            print("lets do assertions:sssssssssssssssssssssssssssssssssssssssssss")
            print("444444444444444444444444444444444444444444444444444444444444444444444ssss")
            assert inserted_user is not None
