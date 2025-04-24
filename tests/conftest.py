import asyncio
import pytest
import pytest_asyncio
import sqlalchemy as sqla
from alembic import command
from alembic.config import Config
from db import get_engine, Base
from sqlalchemy.ext.asyncio import async_sessionmaker


@pytest.fixture(scope="session", autouse=True)
def apply_test_migrations():
    print("1. lets load alembic.ini file:")
    # 1. lets load alembic.ini file:
    alembic_cfg = Config("alembic.ini")
    print("2. choose the section we want")
    # 2. choose the section we want
    alembic_cfg.config_ini_section = "testdb"
    print("3. apply the latest migrations -> revision=head")
    # 3. apply the latest migrations -> revision=head
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migration applied successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")


@pytest.fixture(scope="function")
# @pytest_asyncio.fixture(loop_scope="function", autouse=True)
async def db_session(db_engine_fixture):
    engine = get_engine()
    async_session = async_sessionmaker(bind=engine)
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture()
async def db_engine_fixture():
    print(111111111111111111111111)
    engine=get_engine()
    async with engine.begin() as conn:
        print(22222222222222222222222)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        print(33333333333333333333333333)
        await conn.run_sync(Base.metadata.drop_all)
# @pytest_asyncio.fixture(loop_scope="session", autouse=True)
# # @pytest.fixture(scope="session", autouse=True)
# async def tear_down(db_session):
#     print("lets wait for all tests to be finished")
#     print("lets wait for all tests to be finished")
#     yield
#     print("lest delee eveything")
#     engine = get_engine()
#
#     async with engine.begin() as conn:
#         try:
#
#             await conn.run_sync(Base.metadata.drop_all)
#         except Exception as e:
#             print("//////////////////////////////////////////////////////", e)
#             tables = Base.metadata.tables
#             table_names = ", ".join(tables.keys())
#             raw_query = f"DROP TABLE IF EXISTS {table_names};"
#             print(raw_query)
#             async with db_session.begin():
#                 await db_session.execute(sqla.text(raw_query))



# # @pytest_asyncio.fixture(loop_scope="session", autouse=True)
# @pytest.fixture(scope="session", autouse=True)
# async def tear_down():
#     print("lets wait for all tests to be finished")
#     print("1. lets load alembic.ini file:")
#     # 1. lets load alembic.ini file:
#     alembic_cfg = Config("alembic.ini")
#     print("2. choose the section we want")
#     # 2. choose the section we want
#     alembic_cfg.config_ini_section = "testdb"
#     print("3. apply the latest migrations -> revision=head")
#     # 3. apply the latest migrations -> revision=head
#     try:
#         command.upgrade(alembic_cfg, "head")
#         print("Migration applied successfully!")
#     except Exception as e:
#         print(f"Error during migration: {e}")
#     print("lets wait for all tests to be finished")
#     yield
#     print("lest delee eveything")
#     engine = get_engine()
#
#     async with engine.begin() as conn:
#         try:
#
#             await conn.run_sync(Base.metadata.drop_all)
#         except Exception as e:
#             print("//////////////////////////////////////////////////////", e)
#             tables = Base.metadata.tables
#             table_names = ", ".join(tables.keys())
#             raw_query = f"DROP TABLE IF EXISTS {table_names};"
#             print(raw_query)
#
#             await conn.execute(sqla.text(raw_query))


