from fastapi import  APIRouter, Request
from controllers import IncomeController
from models.enums import ResponseStatus
from .schemes import IncomeRequest, DeleteRequest
from datetime import datetime, timezone


income_router = APIRouter()



@income_router.post("/create_income/{user_id}")
async def create_income(request: Request, user_id: int , income_request: IncomeRequest):

    try:
        income_controller = await IncomeController.create_instance(request.app.db_client)


        new_income = await income_controller.create_income(
            user_id= user_id,
            category_name = income_request.category_name,
            source_name = income_request.source_name,
            amount = income_request.amount,
            is_recurring = income_request.is_recurring,
            description = income_request.description,
            recurrence_interval = income_request.recurrence_interval,
            next_due_date = income_request.next_due_date
        )

        if not new_income:
            return {
                "signal": ResponseStatus.FAILED_ADDED_NEW_INCOME.value
            }
        
        return {
            "signal": ResponseStatus.ADDED_NEW_INCOME_SUCCESSFULLY.value,
            "Income_id": new_income.id,
            "user_id": new_income.user_id,
            "category_id": new_income.category_id,
            "source_name": new_income.source_name,
            "amount": new_income.amount,
            "is_recurring":new_income.is_recurring,
            "description": new_income.description,
            "recurrence_interval": new_income.recurrence_interval,
            "next_due_date": new_income.next_due_date

        }
    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }



@income_router.delete("/delete_income/{user_id}")
async def delete_income_by_id(request: Request, user_id: int ,income_id:DeleteRequest):

    try:
        income_controller = await IncomeController.create_instance(request.app.db_client)
        
        deleted_income =  await income_controller.delete_income_by_id(
            user_id = user_id,
            income_id = income_id.income_id
        ) 

        if deleted_income is None:
            return {
                "signal": ResponseStatus.CAN_NOT_DELETED_THE_INCOME.value
            }
        
        return{
            "signal": ResponseStatus.DELETED_INCOME_SUCCESSFULLY.value,
            "Income_id": deleted_income.id,
            "user_id": deleted_income.user_id,
            "category_id": deleted_income.category_id,
            "source_name": deleted_income.source_name,
            "amount": deleted_income.amount,
            "is_recurring":deleted_income.is_recurring,
            "description": deleted_income.description,
            "recurrence_interval": deleted_income.recurrence_interval,
            "next_due_date": deleted_income.next_due_date

        }

    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }