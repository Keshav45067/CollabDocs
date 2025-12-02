
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.config import Config

dsn: str = Config().build_connection_string()
async_engine = create_async_engine(url=dsn, echo=True)


SessionFactory = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass





