from controllers.BaseController import BaseController
from models import UserModel
import logging

logger = logging.getLogger(__name__)


class UserController(BaseController):

    def __init__(self, db_client: object):
        super().__init__()

        self.db_client = db_client

    

    @classmethod
    async def create_instance(cls, db_client: object):
        return cls(db_client)
    

    async def create_user(self, username: str, email:str, hashed_password: str):

        user_model_instance = await UserModel.create_instance(db_client= self.db_client)
        created_user = await user_model_instance.create_user(
            username=username,
            email=email,
            hashed_password=hashed_password
        )

        if not created_user:
            return None   
        
        return created_user