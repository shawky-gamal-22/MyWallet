from .BaseDataModel import BaseDataModel
from .db_schemes import UserBalance
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import timedelta, timezone



class UserBalanceModel(BaseDataModel):
    """
    UserBalanceModel class for interacting with the UserBalance table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an instance of UserBalanceModel.

        :param db_client: The database client/session maker.
        :return: An instance of UserBalanceModel.
        """
        return cls(db_client)
    

    async def create_user_balance(self, user_id: int):
        new_balance = UserBalance(
            user_id= user_id,
            current_balance = 0.0
        )

        async with self.db_client() as session:
            async with session.begin():
                session.add(new_balance)

            await session.refresh(new_balance)
            return new_balance
    
    async def get_balance(self, user_id: int):
        async with self.db_client() as session:
            stmt = select(UserBalance).where(UserBalance.user_id == user_id)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()       
    
    async def update_balance(self, user_id: int , amount_changed: float):
        """
        amount_changed can be +ve (income) or -ve (invoice/spending)
        """

        async with self.db_client() as session:
            stmt = select(UserBalance).where(UserBalance.user_id == user_id)

            result = await session.execute(stmt)
            balance = result.scalar_one_or_none()

            if balance:
                balance.current_balance += amount_changed
                await session.commit()
                await session.refresh(balance)
                return balance
            return None
        
    async def reset_balance(self, user_id: int):
        async with self.db_client() as session:
            stmt = select(UserBalance).where(UserBalance.user_id == user_id)
            result = await session.execute(stmt)

            balance = result.scalar_one_or_none()

            if balance:
                balance.current_balance = 0.0
                await session.commit()
                await session.refresh(balance)
                return balance
            return None
        
