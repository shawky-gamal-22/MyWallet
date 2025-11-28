from fastapi import FastAPI, Depends, APIRouter, UploadFile, File, Request
from helpers.config import get_settings
from controllers import NLPDataController, DataController
from models import InvoiceModel
from models.db_schemes import Invoice
from models.enums import ResponseStatus
from .schemes import DateRangeRequest
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)



nlp_data_router = APIRouter()


@nlp_data_router.post("/extract-tabular-data/{user_id}")
async def extract_tabular_data( request: Request, user_id: int ,file: UploadFile = File(...)):

    try:

        image_bytes  = await file.read()

        data_controller = await DataController.create_instance()
        ocr_object = await NLPDataController.create_instance(request.app.db_client)
        invoice_model = await InvoiceModel.create_instance(request.app.db_client)

        
        img_path = await data_controller.save_uploaded_file(user_id, file)
        
        extracted_row = await ocr_object.extract_tabular_data(image_bytes, user_id=user_id)


        new_invoice = await invoice_model.create_invoice(
            user_id=int(extracted_row['user_id']),
            category_id=int(extracted_row['category_id']),
            invoice_name=extracted_row['invoice_name'],
            total_price=float(extracted_row['total_price']),
            description=extracted_row['description'],
            img_path=str(img_path)
            )

        if not new_invoice:
            return {
                "signal": ResponseStatus.INVOICE_CANNOT_BE_ADDED.value
            }

        return {
            "signal": ResponseStatus.INVOICE_ADDED_SUCCESSFULLY.value,
            "invoice": {
                "id": new_invoice.id,
                "user_id": new_invoice.user_id,
                "category_id": new_invoice.category_id,
                "invoice_name": new_invoice.invoice_name,
                "total_price": new_invoice.total_price,
                "description": new_invoice.description,
                "img_path": new_invoice.img_path
            }
        }

        
    except Exception as e:
        print(f"Error in /extract-tabular-data/: {e}")
        return {
            "signal": ResponseStatus.ERROR.value,
            "error": str(e)
        }



@nlp_data_router.get("/sumarry_range_date/{user_id}")
async def sumarry_range_date(request: Request, user_id: int ,date_range: DateRangeRequest):
    

    nlp_data_controller = await NLPDataController.create_instance(request.app.db_client)

    summary = await nlp_data_controller.extract_summary_for_range_date(user_id, date_range.start_date, date_range.end_date)

    return summary