from fastapi import FastAPI
from routes import base, data, nlp_data, user, category, invoice, income_category, income
from contextlib import asynccontextmanager
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    # await some_async_startup_function()
    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postgres_conn, echo=True)
    
    app.db_client = sessionmaker(
        app.db_engine, class_=AsyncSession, expire_on_commit=False
    )

    yield
    # Shutdown logic here
    # await some_async_shutdown_function()
    await app.db_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp_data.nlp_data_router)
app.include_router(user.user_router)
app.include_router(category.category_router)
app.include_router(invoice.invoice_router)
app.include_router(income.income_router)
app.include_router(income_category.income_category_router)