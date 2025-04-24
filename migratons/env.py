import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from dotenv import load_dotenv
from models import *
from db import Base

load_dotenv()

is_test: str = os.getenv("IS_TEST")
if is_test == "False":
    db_name: str = os.getenv("DB_NAME")
elif is_test == "True":
    db_name: str = os.getenv("TEST_DB_NAME")
db_port: int = int(os.getenv("DB_PORT"))
# db_name: str = os.getenv("DB_NAME")
test_db_name: str = os.getenv("TEST_DB_NAME")
db_port: int = int(os.getenv("DB_PORT"))
db_host: str = os.getenv("DB_HOST")
db_username: str = os.getenv("DB_USERNAME")
db_password: str = os.getenv("DB_PASSWORD")
db_type: str = os.getenv("DB_TYPE")
db_driver: str = os.getenv("DB_SYNC_DRIVER")
dialect: str = f"{db_type}+{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
print("env.py:dialect:   , ", dialect)
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_section_option(section="devdb", name="sqlalchemy.url", value=dialect)
config.set_section_option(section="testdb", name="sqlalchemy.url", value=dialect)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
