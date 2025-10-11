import os 
import shutil
from controllers.BaseController import BaseController
from datetime import timedelta, timezone, date, datetime
from models import IncomeCategoryModel, IncomeModel
import logging

logger = logging.getLogger(__name__)


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


    async def delete_income_by_id(self, user_id: int , income_id: int):

        income_model_object = await IncomeModel.create_instance(db_client= self.db_client)

        deleted_income = await income_model_object.delete_income(
            user_id= user_id,
            income_id= income_id
        )

        if not deleted_income:
            return None

        return deleted_income
    

    async def update_income(self, user_id: int,
                            income_id: int, 
                            category_name: str= None,
                            source_name: str = None,
                            amount: float = None,
                            is_recurring: bool = None,
                            description: str = None,
                            recurrence_interval: str = None,
                            next_due_date: str = None):
        
        income_model_object = await IncomeModel.create_instance(db_client= self.db_client)
        income_category_model_object = await IncomeCategoryModel.create_instance(db_client= self.db_client)

        #Check if income exists 

        income_row = await income_model_object.get_income_by_id(user_id= user_id, income_id= income_id)

        if income_row is None:
            logger.error(f"This income is not exist")
            return None
        
        # Get category_id by its name
        category_id = await income_category_model_object.get_category_id_by_name(category_name= category_name)
        
        updated_data = {
            "category_id": category_id,
            "source_name":source_name,
            "amount": amount,
            "is_recurring": is_recurring,
            "description": description,
            "recurrence_interval": recurrence_interval,
            "next_due_date": next_due_date
        }

        updated_income = await income_model_object.update_income(
            income_id= income_id,
            user_id= user_id,
            updated_data= updated_data
        )

        if updated_income is None:
            logger.error(f"This income is not exist")
            return None
        
        logger.info(f"Updated income successfully")
        return updated_income



    async def update_next_due_date(self, user_id: int, income_id : int , next_due_date: str):


        income_model_object = await IncomeModel.create_instance(db_client= self.db_client)

        if next_due_date and isinstance(next_due_date, str):
            try:
                next_due_date = datetime.strptime(next_due_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
        
        logger.info(f"changed next_due_date into date")


        updated_income = await income_model_object.update_next_due_date(
            user_id= user_id,
            income_id= income_id, 
            next_date= next_due_date
        )

        if updated_income is None:
            logger.error(f"{income_id} does not exists")
            return None
        
        return updated_income


