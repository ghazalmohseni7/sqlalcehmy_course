from datetime import datetime, date
from sqlalchemy import types, ForeignKey, Index, ForeignKeyConstraint , UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from db import Base


#
# class PyUser(Base):
#     # this is how we create table for sqlalchemy version >= 2.0
#     __tablename__ = 'sqla_user'  # psql thinks table names are all lowercase so if you write uppercase letters it cant find them , so alway write tbale names in lower case
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # you should use python types
#     username: Mapped[str] = mapped_column(types.String(100))  # VARCHAR(100)
#     # 3 way to make a column nullable
#     # age: Mapped[Union[int | None]] = mapped_column()
#     age: Mapped[int | None] = mapped_column()
#     work: Mapped[str] = mapped_column(nullable=True)  # TEXT
#
#     """
#     CREATE TABLE users (
#         id SERIAL NOT NULL,
#         username VARCHAR(100) NOT NULL,
#         age INTEGER,
#         work VARCHAR,
#         PRIMARY KEY (id)
#     )
#     """
#
#
# class PyProduct(Base):
#     __tablename__ = 'sqla_product'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(types.String(100), nullable=False)
#     price: Mapped[float] = mapped_column(nullable=False)
#     available_quantity: Mapped[int] = mapped_column(nullable=False)
#
#     production_date: Mapped[date] = mapped_column(types.Date, nullable=True)
#     expiry_date: Mapped[date] = mapped_column(types.Date, nullable=True)
#     expiry_offset_months: Mapped[int] = mapped_column(nullable=True)  # Example: 12 for a year
#
#
# class PyOrder(Base):
#     __tablename__ = 'sqla_order'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     quantity: Mapped[int] = mapped_column(nullable=False)
#     order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     product_id: Mapped[int] = mapped_column(ForeignKey(PyProduct.id, ondelete="CASCADE"))
#     """
#     CREATE TABLE sqla_order (
#         id SERIAL NOT NULL,
#         quantity INTEGER NOT NULL,
#         order_date TIMESTAMP WITH TIME ZONE NOT NULL,
#         product_id INTEGER NOT NULL,
#         PRIMARY KEY (id),
#         FOREIGN KEY(product_id) REFERENCES sqla_product (id) ON DELETE CASCADE
#     )
#     """

# class UserWithIndex(Base):
#     __tablename__ = "users_with_index"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(types.String(255), nullable=False)
#
#     __table_args__ = (
#         Index("idx_customers_email", "email"),
#         # This creates an index on the email column , the index name is idx_customers_email
#     )
#     """
#     two sql commands will run in one transaction:
#
#     CREATE TABLE users_with_index (
#         id SERIAL NOT NULL,
#         email VARCHAR(255) NOT NULL,
#         PRIMARY KEY (id)
#     )
#
#
#     CREATE INDEX idx_customers_email ON users_with_index (email)
#
#     and this because i use the .begin() method and psql  . for example mysql will run them sequentially
#     """


class ProductWithCompositeUniqueness(Base):
    __tablename__ = "products_compostie_uniqueness"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(types.String(50))
    supplier_id: Mapped[int] = mapped_column()

    __table_args__ = (
        UniqueConstraint("name", "supplier_id", name="uq_product_supplier"),
    )
    """
    CREATE TABLE products_compostie_uniqueness (
        id SERIAL NOT NULL,
        name VARCHAR(50) NOT NULL,
        supplier_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        CONSTRAINT uq_product_supplier UNIQUE (name, supplier_id)
    )
    """


