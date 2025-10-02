from fastapi import  APIRouter, Request
from models import InvoiceModel
from models.enums import ResponseStatus
from .schemes import InvoiceRequest, DateRangeRequest
from datetime import datetime, timezone



invoice_router = APIRouter()

@invoice_router.post("/create_invoices")
async def create_invoice(request: Request, invoice_data: InvoiceRequest):
    """
    Endpoint to create a new invoice.
    :param request: FastAPI Request object to access app state.
    :param invoice_data: InvoiceRequest object containing invoice details.
    :return: JSON response with the created invoice details or error message.
    """
    db_client = request.app.db_client
    invoice_model = await InvoiceModel.create_instance(db_client)

    try:
        new_invoice = await invoice_model.create_invoice(
            user_id=invoice_data.user_id,
            category_id=invoice_data.category_id,
            total_price=invoice_data.total_price,
            description=invoice_data.description,
            img_path=invoice_data.img_path
        )
        return {
            "status": ResponseStatus.ADDED_INVOICE_SUCCESSFULLY.value,
            "data": {
                "invoice_id": new_invoice.id,
                "user_id": new_invoice.user_id,
                "category_id": new_invoice.category_id,
                "total_price": new_invoice.total_price,
                "description": new_invoice.description,
                "img_path": new_invoice.img_path,
                "created_at": new_invoice.created_at
            }
        }
    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }
    

@invoice_router.get("/get_for_a_user/{user_id}")
async def get_invoices_for_user(request: Request, user_id: int):
    """
    Endpoint to retrieve all invoices for a specific user.
    :param request: FastAPI Request object to access app state.
    :param user_id: ID of the user whose invoices are to be retrieved.
    :return: JSON response with the list of invoices or error message.
    """
    db_client = request.app.db_client
    invoice_model = await InvoiceModel.create_instance(db_client)

    try:
        invoices = await invoice_model.get_all_invoices_by_user(user_id)
        invoice_list = [
            {
                "invoice_id": invoice.id,
                "user_id": invoice.user_id,
                "category_id": invoice.category_id,
                "total_price": invoice.total_price,
                "description": invoice.description,
                "img_path": invoice.img_path,
                "created_at": invoice.created_at
            }
            for invoice in invoices
        ]
        return {
            "status": ResponseStatus.GET_INVOICES_FOR_USER_SUCCESS.value,
            "data": invoice_list
        }
    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }


@invoice_router.get("/get_invoice_by_date_range/{user_id}")
async def get_invoices_by_date_range(request: Request, user_id: int, date_range: DateRangeRequest):
    """
    Endpoint to retrieve invoices for a user within a specific date range.
    :param request: FastAPI Request object to access app state.
    :param user_id: ID of the user whose invoices are to be retrieved.
    :param start_date: Start date of the range in 'YYYY-MM-DD' format.
    :param end_date: End date of the range in 'YYYY-MM-DD' format.
    :return: JSON response with the list of invoices or error message.
    """

    db_client = request.app.db_client
    invoice_model = await InvoiceModel.create_instance(db_client)

    try:
        start_dt = datetime.strptime(date_range.start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(date_range.end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

        invoices = await invoice_model.get_invoice_by_date_range(user_id, start_dt, end_dt)
        invoice_list = [
            {
                "invoice_id": invoice.id,
                "user_id": invoice.user_id,
                "category_id": invoice.category_id,
                "invoice_name": invoice.invoice_name,
                "total_price": invoice.total_price,
                "description": invoice.description,
                "img_path": invoice.img_path,
                "created_at": invoice.created_at
            }
            for invoice in invoices
        ]
        return {
            "status": ResponseStatus.GET_INVOICES_FOR_USER_SUCCESS_IN_RANGE_DATE.value,
            "data": invoice_list
        }
    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }
    

@invoice_router.post("/delete_invoice/{invoice_id}")
async def delete_invoice(request: Request, invoice_id: int):
    """
    Endpoint to delete an invoice by its ID.
    :param request: FastAPI Request object to access app state.
    :param invoice_id: ID of the invoice to be deleted.
    :return: JSON response indicating success or failure of the deletion.
    """
    db_client = request.app.db_client
    invoice_model = await InvoiceModel.create_instance(db_client)

    try:
        success = await invoice_model.delete_invoice(invoice_id)
        if success:
            return {
                "status": ResponseStatus.DELETE_INVOICE_SUCCESS.value,
                "message": f"Invoice with ID {invoice_id} deleted successfully."
            }
        else:
            return {
                "status": ResponseStatus.ERROR.value,
                "message": f"Invoice with ID {invoice_id} not found."
            }
    except Exception as e:
        return {
            "status": ResponseStatus.ERROR.value,
            "message": str(e)
        }