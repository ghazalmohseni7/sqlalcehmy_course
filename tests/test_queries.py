import random
import pytest
import sqlalchemy as sqla
from faker import Faker
from models import *

fake = Faker()


# @pytest.mark.asyncio
# def test_a(async_session):
#     print(1111111111111111111111111111,type(async_session))
#     assert True
# class TestQueries:
#     @pytest.mark.asyncio
#     async def test_insert(self, db_session):
#         # arrange
#         category = Category(
#             name=fake.word(),
#         )
#
#         async with db_session.begin():
#             # act
#             db_session.add(category)
#             # assert
#             result = await db_session.execute(
#                 sqla.select(Category).where(Category.name == category.name)
#             )
#             inserted_user = result.scalar_one_or_none()
#             print("lets do assertions:sssssssssssssssssssssssssssssssssssssssssss")
#             print("444444444444444444444444444444444444444444444444444444444444444444444ssss")
#             assert inserted_user is not None





# class TestInsert: # when it was inside the class type(async_session1) was  instance of TestInsert, i donw know why
@pytest.mark.asyncio
async def test_insert_category(async_session1):
    print(1111111111111111111111111111, type(async_session1))
    import asyncio
    loop = asyncio.get_event_loop()
    print(f"***************************************************Event Loop ID (Fixture test_insert_category): {id(loop)}")
    # try:
    new_cat = Category(name=fake.word())
    async_session1.add(new_cat)
    await async_session1.commit()
    await async_session1.refresh(new_cat)
    # except Exception as e:
    #     print(2222222222222222222222,e)

    assert new_cat.id is not None
    # assert new_cat.name == new_cat