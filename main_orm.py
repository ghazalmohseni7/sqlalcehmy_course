import sys
import random
import asyncio
from faker import Faker
import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import async_sessionmaker
from models import *
from db import get_engine

fake = Faker()

if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def insert_user_with_session():
    engine = get_engine()
    async_session = async_sessionmaker(bind=engine)  # this is a class
    user = PyUser(
        username=fake.word(),
        age=random.randint(1, 100),
        work=fake.word()
    )  # this is a dataclass just for now
    async with async_session() as session:
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


if __name__ == "__main__":
    res = asyncio.run(insert_user_with_session())
    print("main : insert_user_with_session : ", res)
