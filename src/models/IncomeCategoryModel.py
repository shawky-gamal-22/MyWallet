from .BaseDataModel import BaseDataModel
from .db_schemes import IncomeCategory
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import timedelta, timezone, date


class IncomeCategoryModel(BaseDataModel):

    """
    IncomeCategoryModel class for interacting with the income_categories table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """

    def __init__(self, db_client):
        super().__init__(db_client=db_client)


        self.db_client = db_client


    @classmethod
    async def create_instance(cls, db_client: object):

        """
        Asynchronous factory method to create an instance of IncomeCategoryModel.

        :param db_client: The database client/session maker.
        :return: An instance of IncomeCategoryModel.
        """

        return cls(db_client)
    
    async def create_category(self, name: str, description: str= None):
        async with self.db_client() as session:
            async with session.begin():
                income_category = IncomeCategory(
                    name = name,
                    description = description
                )

                session.add(income_category)
            await session.refresh(income_category)
            return income_category
        
    
    async def get_all_categories(self ,page_no: int = 1 , page_size: int = 10) :

        async with self.db_client() as session:
            stmt = select(IncomeCategory).offset((page_no-1)*page_size).limit(page_size)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def get_category_by_id(self, category_id: int):
        async with self.db_client() as session:
            stmt = select(IncomeCategory).where(IncomeCategory.id == category_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        
    async def update_category(self, category_id:int , name: str= None, description: str = None):

        category = await self.get_category_by_id(category_id= category_id)

        if not category: 
            return None
        
        if name :
            category.name= name
        if description:
            category.description = description

        async with self.db_client() as session: 
            async with session.begin():
                session.add(category)

            await session.refresh(category)
            return category
        
    async def delete_category(self, category_id: int):
        category = await self.get_category_by_id(category_id= category_id)

        if not category :
            return None
        
        async with self.db_client() as session:
            async with session.begin():
                session.delete(category)
            
        return category