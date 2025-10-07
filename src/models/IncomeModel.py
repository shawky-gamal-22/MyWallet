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
            result = await session.execute(stmt)
            result = result.scalars().all()
            return result
        
    
    async def get_income_by_id(self, user_id:int , income_id:int):
        async with self.db_client() as session:
            stmt = select(Income).where(Income.id == income_id, Income.user_id == user_id)
            result = await session.execute(stmt)
            result = result.scalar_one_or_none()

            return result
        
    async def update_income(self, income_id, user_id:int, updated_data: dict):

        income = await self.get_income_by_id(income_id = income_id, user_id = user_id)

        if not income:
            return None
        
        async with self.db_client() as session:
            async with session.begin():
        
                for key, value in updated_data.items():
                    setattr(income, key, value)
                session.add(income)

            await session.refresh(income)
            return income
    
    async def delete_income(self, income_id: int, user_id: int):

        income = await self.get_income_by_id(income_id= income_id , user_id= user_id)

        if income:
            async with self.db_client() as session:
                async with session.begin():
                    session.delete(income)
        
        return income


    async def get_total_income_by_date_range(self, user_id:int, start_date:datetime, end_date: datetime):
        end_at = end_date + timedelta(days=1)

        async with self.db_client() as session:
            stmt = select(func.sum(Income.amount)).where(
                Income.user_id == user_id,
                Income.created_at >= start_date,
                Income.created_at < end_at  # less than next day
            )

            result = await session.execute(stmt).scalar()

            return result or 0.0
        
    async def get_incomes_by_category(self, user_id: int , category_id:int):
        async with self.db_client() as session:
            stmt = select(Income).where(
                Income.user_id == user_id,
                Income.category_id == category_id
            )
            results = await session.execute(stmt).scalars().all()

            return results
        
    async def get_recurring_incomes_due_today(self, user_id:int):
        today = date.today()

        async with self.db_client() as session:
            stmt = select(Income).where(
                Income.user_id == user_id,
                Income.is_recurring == True,
                Income.next_due_date <= today
            )

            result = await session.execute(stmt).scalars().all()

            return result
        
    async def update_next_due_date(self, user_id: int ,income_id: int , next_date: date):
        result = await self.get_income_by_id(user_id= user_id, income_id= income_id)

        if not result :
            return None
        
        result.next_due_date = next_date

        await self.db_client().commit()
        await self.db_client().refresh(result)
        return result
    

    