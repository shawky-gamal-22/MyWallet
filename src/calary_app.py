from celery import Celery
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


settings = get_settings()

async def get_setup_utils():

    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    db_engine = create_async_engine(postgres_conn, echo=True)
    
    db_client = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )


    return (db_engine, db_client)



# celery_app = Celery(
#     "MyWallet",
#     broker=
#     backend=
# )