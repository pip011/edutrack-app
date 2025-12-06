from typing                     import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio     import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio     import AsyncAttrs
from sqlalchemy.ext.asyncio     import create_async_engine
from sqlalchemy.orm             import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///./backend/database/database.db", echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def init_db(reset=False):
    from . import models
    
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys = ON"))
        
        if reset:
            await conn.run_sync(Base.metadata.drop_all)
            print("База данных удалена")
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")