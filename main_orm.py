import sys
import random
import asyncio
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
    async_session = async_sessionmaker(bind=engine)
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


if __name__ == "__main__":
    # res = asyncio.run(insert_user_with_session())
    # print("main : insert_user_with_session : ", res)
    # asyncio.run(select_star_user())
    asyncio.run(select_with_where())
