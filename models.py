from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
from db import Base


class User(Base):
    # this is how we create table for sqlalchemy version >= 2.0
    __tablename__ = 'Users'
    id: Mapped[Integer] = mapped_column(primary_key=True, autoincrement=True)
