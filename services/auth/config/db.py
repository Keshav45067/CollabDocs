
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from models.user import User
from config.config import Config

dsn: str = Config().build_connection_string()
async_engine = create_async_engine(url=dsn)


SessionFactory = async_sessionmaker(async_engine, expire_on_commit=False)





