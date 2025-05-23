import os
from typing import Any
from datetime import datetime
from functools import lru_cache
from dotenv import load_dotenv
from sqlalchemy import types
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import declarative_base, DeclarativeBase

load_dotenv()


@lru_cache
def get_engine() -> AsyncEngine:
    is_test: str = os.getenv("IS_TEST")
    if is_test == "False":
        db_name: str = os.getenv("DB_NAME")
    elif is_test == "True":
        db_name: str = os.getenv("TEST_DB_NAME")
    db_port: int = int(os.getenv("DB_PORT"))
    db_host: str = os.getenv("DB_HOST")
    db_username: str = os.getenv("DB_USERNAME")
    db_password: str = os.getenv("DB_PASSWORD")
    db_type: str = os.getenv("DB_TYPE")
    db_driver: str = os.getenv("DB_DRIVER")
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW"))
    dialect: str = f"{db_type}+{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_async_engine(url=dialect, pool_size=db_pool_size, max_overflow=db_max_overflow, echo=True)


@lru_cache
def get_base() -> Any:
    # used for sqlalchemy veriosn < 2.0
    return declarative_base()


class Base(DeclarativeBase):
    # used for sqlalchemy veriosn >=2.0
    type_annotation_map = {
        datetime: types.DateTime(timezone=True),  # from now on in this project every datetime column has timezone too
    }
