import asyncio
import pytest
from db import get_engine, Base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


@pytest.fixture(scope="session")
def event_loop():
    # this fixture returns the asyncio event loop
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_event_loop() is deprecated and python suggest using get_running_event but it didnt work for me
    print(f"***************************************************clsEvent Loop ID (Fixture event_loop): {id(loop)}")
    yield loop
    # loop.close()


# Async engine fixture for creating the engine
@pytest.fixture(scope="session")
async def async_engine():
    engine = get_engine()  # Ensure get_engine is correctly implemented elsewhere
    loop = asyncio.get_event_loop()
    # this loop here is just for the print , there is no other usage

    print(f"***************************************************Event Loop ID (Fixture async_engine): {id(loop)}")
    yield engine
    await engine.dispose()


# Setup and teardown database fixture
@pytest.fixture(scope="session", autouse=True)
async def setup_database(async_engine):
    # this loop here is just for the print , there is no other usage
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
async def async_session(async_engine):
    # this loop here is just for the print , there is no other usage
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
