# import asyncio
# import pytest
# import pytest_asyncio
# import sqlalchemy as sqla
# from alembic import command
# from alembic.config import Config
# from db import get_engine, Base
# from sqlalchemy.ext.asyncio import async_sessionmaker
#
#
# @pytest.fixture(scope="session", autouse=True)
# def apply_test_migrations():
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
#
#
# @pytest.fixture(scope="function")
# # @pytest_asyncio.fixture(loop_scope="function", autouse=True)
# async def db_session(db_engine_fixture):
#     engine = get_engine()
#     async_session = async_sessionmaker(bind=engine)
#     async with async_session() as session:
#         yield session
#
# @pytest_asyncio.fixture()
# async def db_engine_fixture():
#     print(111111111111111111111111)
#     engine=get_engine()
#     async with engine.begin() as conn:
#         print(22222222222222222222222)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         print(33333333333333333333333333)
#         await conn.run_sync(Base.metadata.drop_all)
# # @pytest_asyncio.fixture(loop_scope="session", autouse=True)
# # # @pytest.fixture(scope="session", autouse=True)
# # async def tear_down(db_session):
# #     print("lets wait for all tests to be finished")
# #     print("lets wait for all tests to be finished")
# #     yield
# #     print("lest delee eveything")
# #     engine = get_engine()
# #
# #     async with engine.begin() as conn:
# #         try:
# #
# #             await conn.run_sync(Base.metadata.drop_all)
# #         except Exception as e:
# #             print("//////////////////////////////////////////////////////", e)
# #             tables = Base.metadata.tables
# #             table_names = ", ".join(tables.keys())
# #             raw_query = f"DROP TABLE IF EXISTS {table_names};"
# #             print(raw_query)
# #             async with db_session.begin():
# #                 await db_session.execute(sqla.text(raw_query))
#
#
#
# # # @pytest_asyncio.fixture(loop_scope="session", autouse=True)
# # @pytest.fixture(scope="session", autouse=True)
# # async def tear_down():
# #     print("lets wait for all tests to be finished")
# #     print("1. lets load alembic.ini file:")
# #     # 1. lets load alembic.ini file:
# #     alembic_cfg = Config("alembic.ini")
# #     print("2. choose the section we want")
# #     # 2. choose the section we want
# #     alembic_cfg.config_ini_section = "testdb"
# #     print("3. apply the latest migrations -> revision=head")
# #     # 3. apply the latest migrations -> revision=head
# #     try:
# #         command.upgrade(alembic_cfg, "head")
# #         print("Migration applied successfully!")
# #     except Exception as e:
# #         print(f"Error during migration: {e}")
# #     print("lets wait for all tests to be finished")
# #     yield
# #     print("lest delee eveything")
# #     engine = get_engine()
# #
# #     async with engine.begin() as conn:
# #         try:
# #
# #             await conn.run_sync(Base.metadata.drop_all)
# #         except Exception as e:
# #             print("//////////////////////////////////////////////////////", e)
# #             tables = Base.metadata.tables
# #             table_names = ", ".join(tables.keys())
# #             raw_query = f"DROP TABLE IF EXISTS {table_names};"
# #             print(raw_query)
# #
# #             await conn.execute(sqla.text(raw_query))
#
#


import asyncio
import pytest
from db import get_engine, Base
from sqlalchemy.ext.asyncio import async_sessionmaker , AsyncSession


# @pytest.fixture(scope="session")
# def event_loop():
#     """Create a session-wide event loop."""
#     """
#     By default, pytest-asyncio sets up a new event loop for each test function but with this fixture we are telling pytest to ue this event loop for all of the tests
#     """
#     # setUp
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     # tearDown
#     loop.close()
#
#
# @pytest.fixture(scope="session")
# async def async_engine():
#     engine = get_engine()
#     yield engine
#     await engine.dispose()
#
#
# @pytest.fixture(scope="session", autouse=True)
# async def setup_database(async_engine):
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
#
# @pytest.fixture
# async def async_session1(async_engine):
#     async_session_factory = async_sessionmaker(
#         bind=async_engine,
#         expire_on_commit=False,
#         class_=AsyncSession,
#     )
#     async with async_session_factory() as session:
#         yield session



# @pytest.fixture(scope="session")
# def event_loop():
#     # this fixture override the asyncio loop
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     asyncio.set_event_loop(loop) # this makes all to use one loop
#     yield loop
#     loop.close()
#""" with this fizture and commenting the setiip fixtue everything works"""

@pytest.fixture(scope="session")
def event_loop():
    # this fixture returns the asyncio event loop
    loop = asyncio.get_event_loop()
    print(f"***************************************************clsEvent Loop ID (Fixture event_loop): {id(loop)}")
    yield loop
    # loop.close()


# Async engine fixture for creating the engine
@pytest.fixture(scope="session")
async def async_engine():
    engine = get_engine()  # Ensure get_engine is correctly implemented elsewhere
    loop = asyncio.get_event_loop()
    print(f"***************************************************Event Loop ID (Fixture async_engine): {id(loop)}")
    yield engine
    await engine.dispose()

# Setup and teardown database fixture
@pytest.fixture(scope="session", autouse=True)
async def setup_database(async_engine):
    loop = asyncio.get_event_loop()
    print(f"***************************************************Event Loop ID (Fixture setup_database): {id(loop)}")
    # Set up the database (create tables)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Tear down the database (drop tables)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Async session fixture
@pytest.fixture
async def async_session1(async_engine):
    loop = asyncio.get_event_loop()
    print(f"***************************************************Event Loop ID (Fixture async_session1): {id(loop)}")
    # Create a session factory
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=True,
        class_=AsyncSession,  # Ensure you're using AsyncSession
    )
    # Open a new session and yield it for test usage
    async with async_session_factory() as session:
        yield session