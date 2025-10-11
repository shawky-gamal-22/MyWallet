from fastapi import  APIRouter, Request
from controllers import IncomeController
from models.enums import ResponseStatus
from .schemes import IncomeRequest, DeleteRequest, UpdateRequest, UpdateNextDueDateRequest
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


@income_router.post("/update_income/{user_id}")
async def update_income(request: Request, user_id: int, update_request: UpdateRequest):

    try:
        income_controller = await IncomeController.create_instance(db_client= request.app.db_client)

        updated_income = await income_controller.update_income(
            user_id= user_id,
            income_id= update_request.income_id,
            category_name= update_request.category_name,
            source_name = update_request.source_name,
            amount = update_request.amount,
            is_recurring = update_request.is_recurring,
            description = update_request.description,
            recurrence_interval = update_request.recurrence_interval,
            next_due_date = update_request.next_due_date
        )

        if update_income is None:
            return{
                "signal": ResponseStatus.INCOME_ID_DOES_NOT_EXISTS.value
            }
        
        return {
            "signal": ResponseStatus.UPDATED_INCOME_SUCCESSFULLY.value,
            "Income_id": updated_income.id,
            "user_id": updated_income.user_id,
            "category_id": updated_income.category_id,
            "source_name": updated_income.source_name,
            "amount": updated_income.amount,
            "is_recurring":updated_income.is_recurring,
            "description": updated_income.description,
            "recurrence_interval": updated_income.recurrence_interval,
            "next_due_date": updated_income.next_due_date
        }

    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }



@income_router.post("/update_next_due_date/{user_id}")
async def update_next_due_date(request: Request, user_id: int, update_next_due_date_request: UpdateNextDueDateRequest):

    try:
        income_controller = await IncomeController.create_instance(db_client= request.app.db_client)


        updated_income = await income_controller.update_next_due_date(
            user_id= user_id,
            income_id= update_next_due_date_request.income_id,
            next_due_date= update_next_due_date_request.next_due_date
        )

        if update_income is None:
            return {
                "signal": ResponseStatus.INCOME_ID_DOES_NOT_EXISTS.value
            }
        
        return {
            "signal": ResponseStatus.UPDATED_INCOME_SUCCESSFULLY.value,
            "Income_id": updated_income.id,
            "user_id": updated_income.user_id,
            "category_id": updated_income.category_id,
            "source_name": updated_income.source_name,
            "amount": updated_income.amount,
            "is_recurring":updated_income.is_recurring,
            "description": updated_income.description,
            "recurrence_interval": updated_income.recurrence_interval,
            "next_due_date": updated_income.next_due_date
        }



    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }