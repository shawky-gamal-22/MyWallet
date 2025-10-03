from .BaseController import BaseController
from stores.llm.GroqProvider import GroqProvider
from models import CategoryModel
from stores.OCR import MistralOCR
from typing import List
import json
from models import InvoiceModel, CategoryModel
from datetime import datetime, timezone
import logging
import cv2
import numpy as np
from pdf2image import convert_from_bytes

logger = logging.getLogger(__name__)


class NLPDataController(BaseController):
    def __init__(self, db_client: object):
        super().__init__()

        self.db_client = db_client
        
        
    @classmethod
    async def create_instance(cls, db_client):
        return cls(db_client)

    async def extract_row_data(self, file_bytes: bytes):
        ocr = await MistralOCR.create_instance()

        # Try decode as image
        np_arr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # If it's not an image, maybe it's a PDF
        if image is None:
            try:
                pages = convert_from_bytes(file_bytes)
                # Take first page
                image = np.array(pages[0])
            except Exception as e:
                logger.error(f"File is not an image or valid PDF: {e}")
                raise ValueError("Unsupported file type")

        # Continue preprocessing
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        _, buffer = cv2.imencode(".png", adaptive_thresh)
        image_bytes_ready = buffer.tobytes()

        extracted_text = await ocr.read_image(image_bytes_ready)
        return extracted_text
    
    async def list_categories(self):
        has_records = True
        result = []
        page_no = 1
        page_size = 10

        category_model = await CategoryModel.create_instance(self.db_client)
        while has_records:
            categories = await category_model.get_all_categories(page_no= page_no, page_size= page_size)
            if len(categories) == 0:
                has_records = False
            else:
                for category in categories:
                    result.append({
                        "id": category.id,
                        "name": category.name,
                        "description": category.description
                    })
                page_no += 1

        
        if not result:
            result = None
        
        return result
    

    async def generate_row(self, extracted_text: str, user_id: int, categories: List[str]):

        llm = await GroqProvider.create_instance()

        extracted_row = await llm.generate_row(extracted_text, user_id, categories)

        return extracted_row
    
    async def extract_tabular_data(self, image_bytes: bytes, user_id: int):


        extracted_text = await self.extract_row_data(image_bytes)

        categories = await self.list_categories()

        extracted_row = await self.generate_row(extracted_text, user_id, categories)

        invoice_data = json.loads(extracted_row)

        return invoice_data

        
    async def extract_invoice_for_range_date(self, user_id: int, start_date: str, end_date: str):
        try:

            invoice_model = await InvoiceModel.create_instance(self.db_client)

            logger.info(f"Received date range: {start_date} to {end_date}")

            start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)




            invoices = await invoice_model.get_invoice_by_date_range(user_id, start_dt, end_dt)


            if not invoices:
                return {
                    "data": []
                }

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
                "data": invoice_list
            }
        except Exception as e:
            return {
                "message": str(e)
            }
        

    async def extract_total_spent_for_range_date(self, user_id: int, start_date: str, end_date: str):
        try:
            invoice_model = await InvoiceModel.create_instance(self.db_client)

            logger.info(f"Received date range for total spent: {start_date} to {end_date}")

            start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

            total_spent = await invoice_model.get_total_spent_by_date_range(user_id, start_dt, end_dt)

            if not total_spent:
                total_spent = 0.0

            return {
                "total_spent": total_spent
            }
        except Exception as e:
            return {
                "message": str(e)
            }
        

    async def extract_summary_for_range_date(self, user_id: int, start_date: str, end_date: str):
        try:
            invoice_model = await InvoiceModel.create_instance(self.db_client)
            category_model = await CategoryModel.create_instance(self.db_client)

            logger.info(f"Received date range for summary: {start_date} to {end_date}")

            start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

            invoices = await invoice_model.get_invoice_by_date_range(user_id, start_dt, end_dt)

            total_spent = await invoice_model.get_total_spent_by_date_range(user_id, start_dt, end_dt)

            llm = await GroqProvider.create_instance()

            summary = await llm.summary_invoices_range_date(user_id, start_date, end_date, 
                                                            [ {
                                                                "invoice_id": invoice.id,
                                                                "user_id": invoice.user_id,
                                                                "category_name": await category_model.get_category_by_id(invoice.category_id) if await category_model.get_category_by_id(invoice.category_id) else "Unknown",
                                                                "invoice_name": invoice.invoice_name,
                                                                "total_price": invoice.total_price,
                                                                "description": invoice.description,
                                                                "img_path": invoice.img_path,
                                                                "created_at": str(invoice.created_at)
                                                            } for invoice in invoices], total_spent)
            
            summary = json.loads(summary)

            return summary
        except Exception as e:
            return {
                "message": str(e)
            }