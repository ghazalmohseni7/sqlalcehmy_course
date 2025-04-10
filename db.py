import os
from functools import lru_cache
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

load_dotenv()


@lru_cache
def get_engine() -> AsyncEngine:
    db_name: str = os.getenv("DB_NAME")
    db_port: int = int(os.getenv("DB_PORT"))
    db_host: str = os.getenv("DB_HOST")
    db_username: str = os.getenv("DB_USERNAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_type: str = os.getenv("DB_TYPE")
    db_driver: str = os.getenv("DB_DRIVER")
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW"))
    dialect: str = f"{db_type}+{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_async_engine(url=dialect, pool_size=db_pool_size, max_overflow=db_max_overflow)
