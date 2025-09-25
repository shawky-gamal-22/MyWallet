from fastapi import FastAPI, Depends, APIRouter, UploadFile, File
from helpers.config import get_settings
from stores.OCR import MistralOCR
from stores.llm import GroqProvider

nlp_router = APIRouter()


@nlp_router.post("/extract-tabular-data/")
async def extract_tabular_data(file: UploadFile = File(...), app_settings=Depends(get_settings)):

    image_bytes  = await file.read()

    ocr_object = MistralOCR()
    llm = GroqProvider()
    extracted_text = ocr_object.read_image(image_bytes)

    extracted_row = llm.generate_row(extracted_text)

    return {
        "filename": file.filename,
        "extracted_text": extracted_row
    }