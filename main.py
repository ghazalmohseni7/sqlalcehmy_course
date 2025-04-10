import asyncio
import sys
from sqlalchemy import text
from db import get_engine, Base

from models import *  # if we dont do this then sqlalchemy dont know anything about the existance of the User table so Base can not find it

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def apply_tables() -> None:
    try:

        engine = get_engine()  # Ensure you're using the async engine
        async with engine.begin() as conn:

            # lets check the connection to db:
            result = await conn.execute(text('SELECT version();'))
            version = result.all()[0]  # Get the first column of the first row
            print(f"Connected to: {version}")
            # await conn.run_sync(Base.metadata.drop_all)  # Drop tables if they exist
            await conn.run_sync(Base.metadata.create_all)  # Create the tables
            print("Tables applied successfully.")
            print(
                Base.metadata.tables)  # FacadeDict({'Users': Table('Users', MetaData(), Column('id', Integer(), table=<Users>, primary_key=True, nullable=False), schema=None)})
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(apply_tables())

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
