from .BaseDataModel import BaseDataModel
from .db_schemes import Income
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import timedelta, timezone, date



class IncomeModel(BaseDataModel):
    """
    IncomeModel class for interacting with the incomes table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """

    def __init__(self, db_client):
        super().__init__(db_client= db_client)

        self.db_client = db_client


    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an instance of IncomeModel.

        :param db_client: The database client/session maker.
        :return: An instance of UserModel.
        """
        return cls(db_client)
    
    async def create_income(self, 
                            user_id: int,
                            category_id: int,
                            source_name: str,
                            amount: float,
                            is_recurring: bool,
                            description: str = None,
                            recurrence_interval: str= None,
                            next_due_date: date = None):
        
        """
        Create new income record
        """
        new_income_record = Income(
            user_id = user_id,
            category_id = category_id,
            source_name = source_name,
            amount = amount, 
            is_recurring = is_recurring,
            description = description,
            recurrence_interval = recurrence_interval if recurrence_interval else None,
            next_due_date = next_due_date if next_due_date else None
        )

        async with self.db_client() as session:
            async with session.begin():
                session.add(new_income_record)

            await session.refresh(new_income_record)
            return new_income_record
        
    async def get_all_incomes_for_a_user(self, user_id:int, page_no:int = 1, page_size: int = 10):
        async with self.db_client() as session:
            stmt = select(Income).where(Income.user_id == user_id).offset((page_no-1)*page_size).limit(page_size)
            result = session.execute(stmt)
            result = result.scalars().all()
            return result
        
    
    async def get_income_by_id(self, user_id:int , income_id:int):
        async with self.db_client() as session:
            stmt = select(Income).where(Income.id == income_id, Income.user_id == user_id)
            result = session.execute(stmt)
            result = result.scalar_one_or_none()

            return result
        
    async def update_income(self, income_id, user_id:int, updated_data: dict):

        income = await self.get_income_by_id(income_id = income_id, user_id = user_id)

        if not income:
            return None
        
        for key, value in updated_data.items():
            setattr(income, key, value)

        await self.db_client().commit()
        await self.db_client().refresh(income)
        return income
    
    async def delete_income(self, income_id: int, user_id: int):

        income = await self.get_income_by_id(income_id= income_id , user_id= user_id)

        if income:
            async with self.db_client() as session:
                async with session.begin():
                    session.delete(income)
        
        return income
                
    