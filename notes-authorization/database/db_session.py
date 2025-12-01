from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from authorization_config import Config


engine = create_async_engine(Config.AUTHORIZATION_DATABASE_HOST, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

@asynccontextmanager
async def get_db_session():
    session = SessionLocal()
    try:
        yield session
        await session.commit()
    except exc.SQLAlchemyError as e:
        print(f'Ошибка get_db_session() | {e}')
        await session.rollback()
        raise
    finally:
        await session.close()