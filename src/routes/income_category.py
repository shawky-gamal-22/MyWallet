from fastapi import  APIRouter, Request
from controllers import IncomeCategoryController
from models.enums import ResponseStatus
from .schemes import IncomeCategoryRequest
from datetime import datetime, timezone


income_category_router = APIRouter()


@income_category_router.post("/create_income_category")
async def create_income_category(request: Request, income_category_request:IncomeCategoryRequest):

    name = income_category_request.name
    description = income_category_request.description

    income_category_object = await IncomeCategoryController.create_instance(db_client= request.app.db_client)

    new_income_category = await income_category_object.create_new_income_category(
        name = name,
        description = description
    )

    if new_income_category is None:
        return {
            "signal": ResponseStatus.FAILED_TO_ADD_NEW_INCOME_CATEGORY.value
        }
    
    return{
        "signal" : ResponseStatus.ADDED_NEW_INCOME_CATEGORY_SUCCESSFULLY.value,
        "income_category_name": new_income_category.name,
        "income_category_description": new_income_category.description
    }