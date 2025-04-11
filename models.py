from typing import Union
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from db import Base


class User(Base):
    # this is how we create table for sqlalchemy version >= 2.0
    __tablename__ = 'users' # psql thinks table names are all lowercase so if you write uppercase letters it cant find them , so alway write tbale names in lower case
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # you should use python types
    username: Mapped[str] = mapped_column(String(100))  # VARCHAR(100)
    # 3 way to make a column nullable
    # age: Mapped[Union[int | None]] = mapped_column()
    age: Mapped[int | None] = mapped_column()
    work: Mapped[str] = mapped_column(nullable=True)  # TEXT

    """
    CREATE TABLE users (
        id SERIAL NOT NULL,
        username VARCHAR(100) NOT NULL,
        age INTEGER,
        work VARCHAR,
        PRIMARY KEY (id)
    )
    """

