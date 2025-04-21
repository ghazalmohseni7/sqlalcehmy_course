import sys
import random
import asyncio
from datetime import date
from typing import Dict, Any
from faker import Faker
import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from models import *
from db import get_engine

fake = Faker()

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def insert_user_with_session() -> Dict[str, Any]:
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)  # this is a class
    user = PyUser(
        username=fake.word(),
        age=random.randint(1, 100),
        work=fake.word()
    )  # this is a dataclass just for now
    async with async_session() as session:  # session also is type of AsyncSession
        async with session.begin():
            print("add user to session ")
            session.add(user)  # now the user obj is in session memory / add is not async so no need for await
            print("lets see inside the session memory:")
            for key, obj in session.sync_session.identity_map.items():
                print(f"{key}: {obj}")
            print("/////////////////////////")
            print("add user to db")
            # await session.commit()  # this method will call the flush and commit together / actually cause we write .begine() adnd that is transactional , so we dont need the commit here
            print("lets check to see if it is really in db or not:")
            result = await session.execute(
                sqla.select(PyUser).where(
                    PyUser.username == user.username,
                    PyUser.age == user.age,
                    PyUser.work == user.work
                )
            )
            row = result.first()
            if row:
                print(row._asdict())
            print("lets refresh the session memory: specifically update this user we have ")
            await session.refresh(user)
            return user.to_dict()

        """
        (envsqlalchemy) D:\fastProject\sqlalcehmy_course>python main_orm.py
        add user to session 
        lets see inside the session memory:
        /////////////////////////
        add user to db
        lets check to see if it is really in db or not:
        2025-04-18 18:30:55,910 INFO sqlalchemy.engine.Engine select pg_catalog.version()
        2025-04-18 18:30:55,910 INFO sqlalchemy.engine.Engine [raw sql] ()
        2025-04-18 18:30:55,917 INFO sqlalchemy.engine.Engine select current_schema()
        2025-04-18 18:30:55,917 INFO sqlalchemy.engine.Engine [raw sql] ()
        2025-04-18 18:30:55,922 INFO sqlalchemy.engine.Engine show standard_conforming_strings
        2025-04-18 18:30:55,922 INFO sqlalchemy.engine.Engine [raw sql] ()
        2025-04-18 18:30:55,925 INFO sqlalchemy.engine.Engine BEGIN (implicit)
        2025-04-18 18:30:55,927 INFO sqlalchemy.engine.Engine INSERT INTO sqla_user (username, age, work) VALUES ($1::VARCHAR, $2::INTEGER, $3::VARCHAR) RETURNING sqla_user.id
        2025-04-18 18:30:55,927 INFO sqlalchemy.engine.Engine [generated in 0.00043s] ('chair', 77, 'quality')
        2025-04-18 18:30:55,943 INFO sqlalchemy.engine.Engine SELECT sqla_user.id, sqla_user.username, sqla_user.age, sqla_user.work 
        FROM sqla_user
        WHERE sqla_user.username = $1::VARCHAR AND sqla_user.age = $2::INTEGER AND sqla_user.work = $3::VARCHAR
        2025-04-18 18:30:55,943 INFO sqlalchemy.engine.Engine [generated in 0.00037s] ('chair', 77, 'quality')
        {'PyUser': <models.PyUser object at 0x000002A80B9468C0>}
        lets refresh the session memory: specifically update this user we have
        2025-04-18 18:30:55,956 INFO sqlalchemy.engine.Engine SELECT sqla_user.id, sqla_user.username, sqla_user.age, sqla_user.work
        FROM sqla_user
        WHERE sqla_user.id = $1::INTEGER
        2025-04-18 18:30:55,957 INFO sqlalchemy.engine.Engine [generated in 0.00054s] (2,)
        2025-04-18 18:30:55,958 INFO sqlalchemy.engine.Engine COMMIT
        main : insert_user_with_session :  <models.PyUser object at 0x000002A80B9468C0>

        
        """

        """sql equivalent of session.add: INSERT INTO sqla_user (username, age, work) VALUES ($1::VARCHAR, 
        $2::INTEGER, $3::VARCHAR) RETURNING sqla_user.id"""


async def select_star_user():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyUser)
            result = await session.execute(query)
            res = result.scalars().all()  # actually you can not fetch rows after session ends so write this code before session ends
            print([x.to_dict() for x in res])  # now x is an instance of PyUser so we can apply the to_dict()
    # resall=result.all()
    # print([x._asdict() for x in resall]) # [{'PyUser': <models.PyUser object at 0x000001712E60A380>},
    # # {'PyUser': <models.PyUser object at 0x000001712E60A350>}, {'PyUser': <models.PyUser object at
    # # 0x000001712E60A2F0>}, {'PyUser': <models.PyUser object at 0x000001712E60A290>}, {'PyUser': <models.PyUser
    # # object at 0x000001712E60A230>}, {'PyUser': <models.PyUser object at 0x000001712E60A1D0>}] so in the orm ,
    # # the enigne get the rows of the table(like what we hve in core) but then orm converts the rows to the instances
    # # of the PyUser class , so we need to convert these PyUser classes to dict
    # print("////////////////")
    # print([x._asdict()["PyUser"].to_dict() for x in resall])

    """
    sql equivalent :
    SELECT sqla_user.id, sqla_user.username, sqla_user.age, sqla_user.work 
    FROM sqla_user
    """

    """
    result:
    [{'id': 1, 'username': 'meet', 'age': 46, 'work': 'case'}, {'id': 2, 'username': 'chair', 'age': 77, 'work': 'quality'}, {'id': 3, 'username': 'western', 'age': 14, 'work': 'accept
    '}, {'id': 4, 'username': 'instead', 'age': 54, 'work': 'event'}, {'id': 5, 'username': 'option', 'age': 8, 'work': 'strong'}, {'id': 6, 'username': 'population', 'age': 6, 'work': 'why'}]
    2025-04-18 22:40:17,993 INFO sqlalchemy.engine.Engine COMMIT
    """

    """
    let's explainn something , when in core we say : result.all() it returns a list of rows ,
    but in ORM , this will returns a list or tuples of python objects:[(<PyUser(...)>,), (<PyUser(...)>,), ...] , 
    so print([x._asdict()["PyUser"].to_dict() for x in resall]) wont work on it cause x is a tuple ,
    so we should use .scalars() which extract the first value of all of the tuples and creates a list with them , and we will get list[PyUser] 
    which later we can apply the .to_dict method on them.
    """


async def select_with_where():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyUser).where((PyUser.age >= 20) & (PyUser.age <= 80))
            result = await session.execute(query)
            print([x.to_dict() for x in result.scalars().all()])

    """
    sql equivalent
    SELECT sqla_user.id, sqla_user.username, sqla_user.age, sqla_user.work 
    FROM sqla_user
    WHERE sqla_user.age >= $1::INTEGER AND sqla_user.age <= $2::INTEGER
    """


async def select_some_columns():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyUser.id, PyUser.age).where((PyUser.age >= 10) & (PyUser.age <= 50))
            result = await session.execute(query)
            print([x._asdict() for x in result.all()])
    """
    sql equivalent :
        SELECT sqla_user.id, sqla_user.age
        FROM sqla_user
        WHERE sqla_user.age >= $1::INTEGER AND sqla_user.age <= $2::INTEGER
    """
    """
    cause we do not fetch all columns it returns rows not python objects , so there is no need to use .scalars()
    """


async def delete_user():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            row_query = sqla.select(PyUser).where(PyUser.id == 1)
            row = await session.execute(row_query)
            row_exist = row.scalar_one_or_none()  # this method returns python obj or none
            # delete query:
            if row_exist:
                result = await session.delete(row_exist)

    """
    sql equivalent:
        DELETE FROM sqla_user WHERE sqla_user.id = $1::INTEGER
    """

    """
    note the in core we write : sqla.delete(PyUser).where(PyUser.id==1) but why we first fetch the row and then 
    delete it with session ? cause we are using ORM not core , adn ORM works with session , so data should be in 
    session
    """


async def update_user():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            # load data to session
            result = await session.execute(sqla.select(PyUser).where(PyUser.id == 2))
            user = result.scalar_one_or_none()  # python object or None
            if user:
                user.age = 200
                user.work = "cooko"  # now data is updated
                # session.commit if you are not using the context manager , but now we are using it , so no need to
                # write this line
    """
    sql equivalent:
        UPDATE sqla_user SET age=$1::INTEGER, work=$2::VARCHAR WHERE sqla_user.id = $3::INTEGER
    """
    """
    what terminal says : 
        2025-04-19 14:43:05,035 INFO sqlalchemy.engine.Engine SELECT sqla_user.id, sqla_user.username, sqla_user.age, sqla_user.work 
        FROM sqla_user
        WHERE sqla_user.id = $1::INTEGER
        2025-04-19 14:43:05,036 INFO sqlalchemy.engine.Engine [generated in 0.00072s] (2,)
        2025-04-19 14:43:05,041 INFO sqlalchemy.engine.Engine UPDATE sqla_user SET age=$1::INTEGER, work=$2::VARCHAR WHERE sqla_user.id = $3::INTEGER
        2025-04-19 14:43:05,042 INFO sqlalchemy.engine.Engine [generated in 0.00046s] (200, 'cooko', 2)
        2025-04-19 14:43:05,052 INFO sqlalchemy.engine.Engine COMMIT

    """


async def join():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyProduct, PyOrder).join(PyOrder, PyProduct.id == PyOrder.product_id).where(
                PyOrder.order_date >= date(year=2012, month=1, day=1))
            result = await session.execute(query)
            # result is s list of tuples which the tuple itself contains one obj of PyProduct and one obj of PyOrder
            # so scalars wont work here
            rows = result.all()
            for product, order in rows:
                print(product.to_dict(), order.to_dict())

    """
    some notes: 
    1. in Core we have select_from method and then inside that we use the innerjoin method , 
    while in ORM we just have join method , there is no select_from or innerjion, the name of the class we write in 
    join method is the JOIN table clause ,and in select we should write the name of the both tables, one of them 
    written in join method the other is one is FROM table.
    
    2. cause it returns a list[(table1_obj , table2_obj),(table1_obj , table2_obj),(table1_obj , table2_obj),
    ...] then we can not use scalars() so we need to iterate through
    
    """

    """
    sql equivalent:
        SELECT sqla_product.id, sqla_product.name, sqla_product.price, sqla_product.available_quantity, sqla_product.production_date, sqla_product.expiry_date, sqla_product.expiry_offset_months, sqla_order.id AS id_1, sqla_order.quantity, sqla_order.order_date, sqla_order.product_id
        FROM sqla_product JOIN sqla_order 
        ON sqla_product.id = sqla_order.product_id
    """


async def left_join():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyProduct, PyOrder).outerjoin(PyOrder, PyProduct.id == PyOrder.product_id).where(
                PyOrder.order_date >= date(year=2012, month=1, day=1))
            result = await session.execute(query)
            rows = result.all()
            for product, order in rows:
                print(product.to_dict(), order.to_dict())
    """
    sql equivalent:
        SELECT sqla_product.id, sqla_product.name, sqla_product.price, sqla_product.available_quantity, sqla_product.production_date, sqla_product.expiry_date, sqla_product.expiry_offset_months, sqla_order.id AS id_1, sqla_order.quantity, sqla_order.order_date, sqla_order.product_id
        FROM sqla_product LEFT OUTER JOIN sqla_order ON sqla_product.id = sqla_order.product_id
        WHERE sqla_order.order_date >= $1::DATE
    """


async def right_join():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyProduct, PyOrder).outerjoin(PyProduct, PyOrder.product_id == PyProduct.id).where(
                PyOrder.order_date >= date(year=2012, month=1, day=1))
            result = await session.execute(query)
            rows = result.all()
            for product, order in rows:
                print(product.to_dict(), order.to_dict())

    """
    sql equivalent:
        SELECT sqla_product.id, sqla_product.name, sqla_product.price, sqla_product.available_quantity, sqla_product.production_date, sqla_product.expiry_date, sqla_product.expiry_offset_months, sqla_order.id AS id_1, sqla_order.quantity, sqla_order.order_date, sqla_order.product_id
        FROM sqla_order LEFT OUTER JOIN sqla_product ON sqla_order.product_id = sqla_product.id
        WHERE sqla_order.order_date >= $1::DATE

    """
    """
    so for rigt join just change the join table
    """


async def aggregation_count():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(sqla.func.count(PyUser.id).label("LEN"))
            result = await session.execute(query)
            print(result.first()._asdict())

    """
    sql equivalent:
        SELECT count(sqla_user.id) AS "LEN"
        FROM sqla_user
    """


async def aggregation_sum():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(PyOrder.product_id,
                                sqla.func.sum(PyOrder.quantity).label("order_per_product")).group_by(
                PyOrder.product_id).order_by(PyOrder.product_id)
            result = await session.execute(query)
            print([x._asdict() for x in result.all()])

    """
    sql equivalent:
        SELECT sqla_order.product_id, sum(sqla_order.quantity) AS order_per_product
        FROM sqla_order 
        GROUP BY sqla_order.product_id 
        ORDER BY sqla_order.product_id
    """


async def aggregation_avg():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = (
                sqla.select(PyProduct.id, sqla.func.avg(PyProduct.price * PyOrder.quantity).label("avg_order_price"))
                .outerjoin(PyOrder, PyProduct.id == PyOrder.product_id)
                .group_by(PyProduct.id)
                .order_by(PyProduct.id)
            )
            result = await session.execute(query)
            print([x._asdict() for x in result.all()])
    """
    sql equivalent:
        SELECT sqla_product.id, avg(sqla_product.price * sqla_order.quantity) AS avg_order_price 
        FROM sqla_product 
        LEFT OUTER JOIN sqla_order 
        ON sqla_product.id = sqla_order.product_id 
        GROUP BY sqla_product.id 
        ORDER BY sqla_product.id

    """


async def aggregation_min_max():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = sqla.select(sqla.func.min(PyUser.age).label("child"), sqla.func.max(PyUser.age).label("adult"))
            result = await session.execute(query)
            print([x._asdict() for x in result.all()])
    """
    sql equivalent:
        SELECT min(sqla_user.age) AS child, max(sqla_user.age) AS adult 
        FROM sqla_user
    """


async def aggregation_having():
    engine = get_engine()
    async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)
    async with async_session() as session:
        async with session.begin():
            query = (
                sqla.select(PyProduct.id, sqla.func.avg(PyProduct.price * PyOrder.quantity).label("avg_order_price"))
                .outerjoin(PyOrder, PyProduct.id == PyOrder.product_id)
                .group_by(PyProduct.id)
                .having(sqla.func.avg(PyProduct.price * PyOrder.quantity) > 100)
                .order_by(PyProduct.id)
            )
            result = await session.execute(query)
            print([x._asdict() for x in result.all()])
    """
    sql equivalent:
        SELECT sqla_product.id, avg(sqla_product.price * sqla_order.quantity) AS avg_order_price 
        FROM sqla_product 
        LEFT OUTER JOIN sqla_order 
        ON sqla_product.id = sqla_order.product_id 
        GROUP BY sqla_product.id
        HAVING avg(sqla_product.price * sqla_order.quantity) > $1::INTEGER 
        ORDER BY sqla_product.id

    """


if __name__ == "__main__":
    # res = asyncio.run(insert_user_with_session())
    # print("main : insert_user_with_session : ", res)
    # asyncio.run(select_star_user())
    # asyncio.run(select_with_where())
    # asyncio.run(select_some_columns())
    # asyncio.run(delete_user())
    # asyncio.run(update_user())
    # asyncio.run(join())
    # asyncio.run(left_join())
    # asyncio.run(right_join())
    # asyncio.run(aggregation_count())
    # asyncio.run(aggregation_sum())
    # asyncio.run(aggregation_avg())
    # asyncio.run(aggregation_min_max())
    asyncio.run(aggregation_having())
