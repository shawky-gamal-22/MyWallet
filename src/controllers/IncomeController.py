import os 
import shutil
from controllers.BaseController import BaseController
from datetime import timedelta, timezone, date, datetime
from models import IncomeCategoryModel, IncomeModel


class IncomeController(BaseController):

    def __init__(self, db_client: object):
        super().__init__()

        self.db_client = db_client

    

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)
    

    async def create_income(self, user_id: int ,
                            category_name: str,
                            source_name: str,
                            amount: float,
                            is_recurring: bool,
                            description: str= None,
                            recurrence_interval: str= None,
                            next_due_date: date= None):
        
        income_category_model_object = await IncomeCategoryModel.create_instance(db_client= self.db_client)
        income_model_object = await IncomeModel.create_instance(db_client= self.db_client)


        category_id = await income_category_model_object.get_category_id_by_name(category_name= category_name)

        if next_due_date and isinstance(next_due_date, str):
            try:
                next_due_date = datetime.strptime(next_due_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        new_income = await income_model_object.create_income(
            user_id = user_id,
            category_id = category_id,
            source_name = source_name,
            amount = amount,
            is_recurring = is_recurring, 
            description = description,
            recurrence_interval = recurrence_interval,
            next_due_date = next_due_date
        )

        if not new_income:
            return None
        
        return new_income


        


