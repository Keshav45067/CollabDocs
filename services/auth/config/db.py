
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from models.user import User


async_engine = create_async_engine(url="postgresql+asyncpg://postgres:keshav@localhost:5433/mydb")

session_factory = async_sessionmaker[AsyncSession](async_engine)

# async def get_session():
#     async with session_factory() as session:
#         yield session


async def trial():
    async with session_factory() as async_session:
        user = User(
            name= "keshav",
            email="keshav@f.co",
            password="dsakld"
        )
        async_session.add(user)
        await async_session.commit()

if __name__ == "__main__":
    asyncio.run(trial())



# from collections.abc import AsyncGenerator
# from collections.abc import Generator
# from sqlalchemy.engine import create_engine
# from sqlalchemy.engine import Engine
# from sqlalchemy.ext.asyncio import AsyncEngine
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import Session
# from configs.app_configs import POSTGRES_USER
# from configs.app_configs import POSTGRES_PASSWORD
# from configs.app_configs import POSTGRES_HOST
# from configs.app_configs import POSTGRES_PORT
# from configs.app_configs import POSTGRES_DB


# SYNC_DB_API = "psycopg2"
# ASYNC_DB_API = "asyncpg"


# # global so we don't create more than one engine per process
# # outside of being best practice, this is needed so we can properly pool
# # connections and not create a new pool on every request
# _SYNC_ENGINE: Engine | None = None
# _ASYNC_ENGINE: AsyncEngine | None = None


# def build_connection_string(
#     *,
#     db_api: str = ASYNC_DB_API,
#     user: str = POSTGRES_USER,
#     password: str = POSTGRES_PASSWORD,
#     host: str = POSTGRES_HOST,
#     port: str = POSTGRES_PORT,
#     db: str = POSTGRES_DB,
# ) -> str:
#     return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


# def get_sqlalchemy_engine() -> Engine:
#     global _SYNC_ENGINE
#     if _SYNC_ENGINE is None:
#         connection_string = build_connection_string(db_api=SYNC_DB_API)
#         _SYNC_ENGINE = create_engine(connection_string, pool_size=50, max_overflow=25)
#     return _SYNC_ENGINE


# def get_sqlalchemy_async_engine() -> AsyncEngine:
#     global _ASYNC_ENGINE
#     if _ASYNC_ENGINE is None:
#         connection_string = build_connection_string()
#         _ASYNC_ENGINE = create_async_engine(connection_string)
#     return _ASYNC_ENGINE


# def get_session() -> Generator[Session, None, None]:
#     with Session(get_sqlalchemy_engine(), expire_on_commit=False) as session:
#         yield session


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSession(
#         get_sqlalchemy_async_engine(), expire_on_commit=False
#     ) as async_session:
#         yield async_session
