from .BaseDataModel import BaseDataModel
from .db_schemes import User
from sqlalchemy.future import select



class UserModel(BaseDataModel):
    """
    UserModel class for interacting with the users table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an instance of UserModel.

        :param db_client: The database client/session maker.
        :return: An instance of UserModel.
        """
        return cls(db_client)

    async def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The user object if found, else None.
        """
        async with self.db_client() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user

    async def create_user(self, username: str, email: str, hashed_password: str):
        """
        Create a new user in the database.

        :param username: The username of the new user.
        :param email: The email of the new user.
        :param password_hash: The hashed password of the new user.
        :return: The created user object.
        """
        user_by_email = await self.get_user_by_email(email)
        if user_by_email:
            return None  # User with this email already exists
        
        else:

            async with self.db_client() as session:
                async with session.begin():
                    new_user = User(username=username, email=email, hashed_password=hashed_password)
                    session.add(new_user)
                
                await session.refresh(new_user)
                return new_user
        
    async def get_user_by_email(self, email: str):
        """
        Retrieve a user by their email.

        :param email: The email of the user to retrieve.
        :return: The user object if found, else None.
        """
        async with self.db_client() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user
    
    async def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user by their email and password.

        :param email: The email of the user to authenticate.
        :param password: The password of the user to authenticate.
        :return: The user object if authentication is successful, else None.
        """
        user = await self.get_user_by_email(email)
        if user :
            return user
        return None
    
    async def list_users(self, skip: int = 0, limit: int = 10):
        """
        List users with pagination.

        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of user objects.
        """
        async with self.db_client() as session:
            stmt = select(User).offset(skip).limit(limit)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return users
        
    async def delete_user(self, user_id: int):
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete.
        :return: True if deletion was successful, else False.
        """
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user = result.scalars().first()
                if user:
                    await session.delete(user)
                    return True
            return False
    
