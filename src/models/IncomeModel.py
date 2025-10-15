from .BaseDataModel import BaseDataModel
from .db_schemes import Income, UserBalance
from .UserBalanceModel import UserBalanceModel
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import func, or_
from sqlalchemy.future import select
from datetime import timedelta, timezone, date
from dateutil.relativedelta import relativedelta



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
        :return: An instance of IncomeModel.
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
        

        async with self.db_client() as session:
            async with session.begin():
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
                session.add(new_income_record)

                stmt = select(UserBalance).where(UserBalance.user_id == user_id)
                result = await session.execute(stmt)
                user_balance = result.scalar_one_or_none()

                if not user_balance:
                    raise ValueError(f"No balance found for user_id={user_id}")
                
                user_balance.current_balance += amount 
                session.add(user_balance)


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
        
    async def update_income(self, income_id: int, user_id: int, updated_data: dict):
        async with self.db_client() as session:
            async with session.begin():
                # Fetch the income record
                stmt = select(Income).where(Income.id == income_id, Income.user_id == user_id)
                result = await session.execute(stmt)
                income = result.scalar_one_or_none()

                if not income:
                    raise ValueError(f"No income found with income_id={income_id}")

                # Check if amount needs to be updated (and adjust user balance)
                new_amount = updated_data.get("amount")
                if new_amount is not None and new_amount != income.amount:
                    diff = new_amount - income.amount

                    # Fetch user balance once
                    balance_stmt = select(UserBalance).where(UserBalance.user_id == user_id)
                    result = await session.execute(balance_stmt)
                    user_balance = result.scalar_one_or_none()

                    if not user_balance:
                        raise ValueError(f"No balance found for user_id={user_id}")

                    user_balance.current_balance += diff
                    income.amount = new_amount  # update amount manually
                    # remove "amount" from dict so it doesn't get set again below
                    updated_data.pop("amount")

                # Update other fields dynamically
                for key, value in updated_data.items():
                    if hasattr(income, key) and value is not None:
                        setattr(income, key, value)

            # refresh after commit
            await session.refresh(income)
            return income
    
    async def delete_income(self, income_id: int, user_id: int):

        income = await self.get_income_by_id(income_id= income_id , user_id= user_id)

        if income:
            async with self.db_client() as session:
                async with session.begin():
                    await session.delete(income)
        
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
    

    async def cron_task_for_recurring_incomes(self, today: date, page_no: int, page_size: int):

        async with self.db_client() as session:
            stmt = select(Income).where(
                Income.is_recurring == True,
                Income.next_due_date <= today,
                or_(
                    Income.last_run_date == None,
                    Income.last_run_date < Income.next_due_date
                )
            ).offset((page_no-1)*page_size).limit(page_size)

            result = await session.execute(stmt)
            incomes = result.scalars().all()

            if not incomes:
                return []
            
            # prefetch balances
            user_ids = [income.user_id for income in incomes]
            stmt = select(UserBalance).where(UserBalance.user_id.in_(user_ids))
            result = await session.execute(stmt)
            balances= {b.user_id: b for b in result.scalars().all()}

            for income in incomes:

                balance = balances.get(income.user_id)

                if not balance:
                    continue # skip users without balance
                
                balance.current_balance += income.amount

                if income.recurrence_interval == "daily":
                    income.next_due_date += timedelta(days=1)
                elif income.recurrence_interval == "weekly":
                    income.next_due_date += timedelta(weeks=1)
                elif income.recurrence_interval == "monthly":
                    income.next_due_date += relativedelta(months=1)
                elif income.recurrence_interval == "yearly":
                    income.next_due_date += relativedelta(years=1)
                income.last_run_date = today

            await session.commit()
            return incomes
            




