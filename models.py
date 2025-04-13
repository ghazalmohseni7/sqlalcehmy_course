from datetime import datetime, date
from sqlalchemy import types, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import Base


class PyUser(Base):
    # this is how we create table for sqlalchemy version >= 2.0
    __tablename__ = 'sqla_user'  # psql thinks table names are all lowercase so if you write uppercase letters it cant find them , so alway write tbale names in lower case
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # you should use python types
    username: Mapped[str] = mapped_column(types.String(100))  # VARCHAR(100)
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


class PyProduct(Base):
    __tablename__ = 'sqla_product'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(types.String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    available_quantity: Mapped[int] = mapped_column(nullable=False)

    production_date: Mapped[date] = mapped_column(types.Date, nullable=True)
    expiry_date: Mapped[date] = mapped_column(types.Date, nullable=True)
    expiry_offset_months: Mapped[int] = mapped_column(nullable=True)  # Example: 12 for a year


class PyOrder(Base):
    __tablename__ = 'sqla_order'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    product_id: Mapped[int] = mapped_column(ForeignKey(PyProduct.id, ondelete="CASCADE"))
    product: Mapped["PyProduct"] = relationship()

    """
    CREATE TABLE sqla_order (
        id SERIAL NOT NULL,
        quantity INTEGER NOT NULL,
        order_date TIMESTAMP WITH TIME ZONE NOT NULL,
        product_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(product_id) REFERENCES sqla_product (id) ON DELETE CASCADE
    )
    """
