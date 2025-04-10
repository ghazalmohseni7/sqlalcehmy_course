from sqlalchemy.orm import mapped_column, Mapped
from db import Base


class User(Base):
    # this is how we create table for sqlalchemy version >= 2.0
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # you should use python types
