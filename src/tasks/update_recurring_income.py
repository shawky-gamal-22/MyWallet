from celery_app import get_setup_utils, celery_app
from helpers.config import get_settings
from models.enums import ResponseStatus
from models import IncomeModel
from asgiref.sync import async_to_sync
import asyncio
import logging
from datetime import date

logger = logging.getLogger(__name__)

@celery_app.task(
    bind=True,
    name="tasks.update_recurring_income.update_recurring_income",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def update_recurring_income(self):
    logger.info("🚀 Celery Beat triggered: update_recurring_income started.")
    return asyncio.run(
        _update_recurring_income(self)
    )
    # logger.info("✅ Celery Beat completed: update_recurring_income finished.")

async def _update_recurring_income(task_instance):
    db_engine, db_client = None, None
    try:
        db_engine, db_client = get_setup_utils()
        income_model = await IncomeModel.create_instance(db_client=db_client)

        today = date.today()
        page_no, page_size = 1, 100

        total_processed = 0

        while True:
            incomes = await income_model.cron_task_for_recurring_incomes(
                today=today,
                page_no=page_no,
                page_size=page_size,
            )

            if not incomes:
                break

            processed_count = len(incomes)
            total_processed += processed_count

            logger.info(f"Processed page {page_no}: {processed_count} records.")
            page_no += 1

        logger.info(f"✅ Finished processing {total_processed} recurring incomes for {today}")

    except Exception as e:
        logger.error(f"❌ Task failed: {str(e)}", exc_info=True)
        raise
    finally:
        if db_engine:
            try:
                await db_engine.dispose()
            except Exception as e:
                logger.error(f"Error during DB cleanup: {str(e)}")
