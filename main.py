import asyncio
import sys
from random import uniform, randint
from faker import Faker
import sqlalchemy as sqla
from sqlalchemy import text
from db import get_engine, Base

from models import *  # if we dont do this then sqlalchemy dont know anything about the existance of the User table so Base can not find it

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

fake = Faker()


async def apply_tables() -> None:
    try:

        engine = get_engine()  # Ensure you're using the async engine
        async with engine.begin() as conn:

            # lets check the connection to db:
            # result = await conn.execute(text('SELECT version();'))
            # version = result.all()[0]  # Get the first column of the first row
            # print(f"Connected to: {version}")
            await conn.run_sync(Base.metadata.drop_all)  # Drop tables if they exist
            await conn.run_sync(Base.metadata.create_all)  # Create the tables
            print("Tables applied successfully.")
            print(
                Base.metadata.tables)  # FacadeDict({'Users': Table('Users', MetaData(), Column('id', Integer(), table=<Users>, primary_key=True, nullable=False), schema=None)})
    except Exception as e:
        print(f"Error: {e}")


async def insert_product():
    engine = get_engine()
    query = sqla.insert(PyProduct).values({
        PyProduct.name: fake.word(),
        PyProduct.price: round(uniform(1.0, 100.0), 2),
        PyProduct.available_quantity: randint(1, 50),
        #
        # PyProduct.production_date: ,
        # PyProduct.expiry_date:,
        # PyProduct.expiry_offset_months: ,
    }

    ).returning(PyProduct.id)
    async with engine.begin() as conn:
        result = await conn.execute(query)
        # print("insert result: ", result.all()) # returns a list contains a tupple which in tuple ther is a id
        # print("insert result: ", result.first()) # returns  a tuple
        # list_result=result.all()
        firts_resukt = result.first()
        # print("insert result: ", list_result[0]) # returns  a tuple
        # print("insert result: ", firts_resukt._tuple())# returns  a tuple
        print("insert result: ", firts_resukt._asdict())  # returns  a dict : {'id': 12}
        """
        you can not do this:
        result.all()
        result.first()
        cause the first line will fetch data from db and then there is nothing for second line to fetch
        """


async def select_star():
    engine = get_engine()
    query = sqla.select(PyProduct)
    async with engine.begin() as conn:
        result = await conn.execute(query)
    all_result = result.all()
    print(all_result)  # list of tuples
    for row in all_result:
        print(row)  # reutrns tuple :(12, 'enjoy', 39.05, 18, None, None, None)
        print(
            row._asdict())  # reutrns dict ;{'id': 12, 'name': 'enjoy', 'price': 39.05, 'available_quantity': 18, 'production_date': None, 'expiry_date': None, 'expiry_offset_months': None}


async def select_some_columns():
    engine = get_engine()
    query = sqla.select(PyProduct.id, PyProduct.name)
    async with engine.begin() as conn:
        result = await conn.execute(query)
    all_result = result.all()
    print(all_result)  # list of tuples
    for row in all_result:
        print(row)  # reutrns tuple :(12, 'enjoy', 39.05, 18, None, None, None)
        print(
            row._asdict())  # reutrns dict ;{'id': 12, 'name': 'enjoy', 'price': 39.05, 'available_quantity': 18, 'production_date': None, 'expiry_date': None, 'expiry_offset_months': None}


async def select_with_where():
    engine = get_engine()
    start_date = date(2025, 1, 1)
    end_date = date(2026, 12, 31)
    query = sqla.select(PyProduct).where((PyProduct.production_date >= start_date) &
                                         (PyProduct.expiry_date < end_date))
    query1 = sqla.select(PyProduct).where(PyProduct.price.between(1.0, 6.0))
    async with engine.begin() as conn:
        res = await conn.execute(query)
        res1 = await conn.execute(query1)
    print(res.all())
    print(res1.all())


async def update_product():
    engine = get_engine()
    query = sqla.update(PyProduct).where(PyProduct.id == 1).values({
        PyProduct.price: round(uniform(1.0, 100.0), 2),
        PyProduct.available_quantity: randint(1, 50),
    }).returning(PyProduct)
    async with engine.begin() as conn:
        res = await conn.execute(query)

    print(res.all())




if __name__ == "__main__":
    # asyncio.run(apply_tables())
    # asyncio.run(insert_product())
    # asyncio.run(select_star())
    # asyncio.run(select_some_columns())
    # asyncio.run(select_with_where())
    asyncio.run(update_product())

# from sqlalchemy import create_engine
#
# engine = create_engine("postgresql+psycopg2://user:password@localhost:port/db_name")
#
# # context manager:
# with engine.begin() as conn:
#     result = conn.execute(...)
#
# from sqlalchemy.ext.asyncio import create_async_engine
#
# async_engine = create_async_engine("postgresql+asyncpg://user:password@localhost:port/db_name")
# # context manager:
# async with async_engine.begin() as conn:
#     result = await conn.execute(...)
#
#
# from functools import lru_cache
# from sqlalchemy.ext.asyncio import create_async_engine
#
#
# @lru_cache
# def get_engine():
#     engine = create_async_engine("postgresql+asyncpg://user:password@localhost:port/db_name", pool_si8ze=5,
#                                  max_overflow=0)
#     return engine
