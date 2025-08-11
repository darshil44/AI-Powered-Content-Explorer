from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # create any missing tables
        await conn.run_sync(SQLModel.metadata.create_all)

# dependency
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
