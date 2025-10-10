import os 
import shutil
from controllers.BaseController import BaseController
from datetime import timedelta, timezone, date, datetime
from models import IncomeCategoryModel, IncomeModel


class IncomeCategoryController(BaseController):

    def __init__(self, db_client: object):
        super().__init__()

        self.db_client = db_client

    

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)
    

    async def create_new_income_category(self, 
                                        name: str,
                                        description: str= None):
        
        income_category_object = await IncomeCategoryModel.create_instance(db_client= self.db_client)

        new_income_category = await income_category_object.create_category(
            name= name,
            description= description
        )


        if not new_income_category:
            return None
        
        return new_income_category