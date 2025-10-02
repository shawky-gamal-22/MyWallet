from fastapi import  APIRouter, Request
from helpers.config import get_settings
from models import UserModel
from models.enums import ResponseStatus
from .schemes import UserRequest


user_router = APIRouter()



@user_router.post("/create-user/")
async def create_user(request: Request, user: UserRequest):
    
    user_model_instance = await UserModel.create_instance(request.app.db_client)
    created_user = await user_model_instance.create_user(
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password
    )

    if not created_user:
        return{
            "status": ResponseStatus.USER_EMAIL_EXISTS.value
        }   
    
    return {
            "status": ResponseStatus.USER_ADDED_SUCCESS.value,
            "user_id": created_user.id
            }

