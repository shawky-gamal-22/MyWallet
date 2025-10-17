from celery import Celery
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from celery.schedules import crontab

settings = get_settings()

def get_setup_utils():

    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    db_engine = create_async_engine(postgres_conn, echo=True)
    
    db_client = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )


    return (db_engine, db_client)


# Celery app instance
celery_app = Celery(
    "MyWallet",
    broker= settings.CELERY_BROKER_URL,
    backend= settings.CELERY_RESULT_BACKEND,
)
# Import tasks AFTER celery_app is created
celery_app.autodiscover_tasks(['tasks'], force=True)

# Configure celery with essential settings

celery_app.conf.update(
    task_serializer= settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=[
        settings.CELERY_TASK_SERIALIZER
    ],
    task_acks_late= settings.CELERY_TASK_ACKS_LATE,
    task_time_limit= settings.CELERY_TASK_TIME_LIMIT,
    task_ignore_result= False,
    result_expires=3600, 
    worker_concurrency= settings.CELERY_WORKER_CONCURRENCY,

    # Connection settings for better reliability
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    worker_cancel_long_running_tasks_on_connection_loss=True,

    task_routes={
        "tasks.update_recurring_income.update_recurring_income":{"queue":"default"},
        "tasks.update_recurring_invoices.update_recurring_invoices":{"queue":"default"}
    },

    beat_schedule={
        'process_recurring_incomes_every_day':{
            'task': "tasks.update_recurring_income.update_recurring_income",
            #'schedule': crontab(hour=0, minute=0), # 00:00 every day
            'schedule': 15.0, # every 15 seconds
            'args':()

        },
        'process_recurring_invoices_every_day':{
            'task': "tasks.update_recurring_invoices.update_recurring_invoices",
            'schedule': crontab(hour=0, minute=0), # every day at 00:00 AM, Once daily at midnight
            'args': ()
        }
    },
    task_default_queue = "default",
    timezone = 'UTC',
    # Important: Ensure worker state is properly initialized
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


