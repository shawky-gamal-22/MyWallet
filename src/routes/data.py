from fastapi import FastAPI, Depends, APIRouter, UploadFile, File, Request
from helpers.config import get_settings
from stores.OCR import Pytesseract, MistralOCR
from agents.SQLAgent.utils.nodes import check_relevance

data_router = APIRouter()


@data_router.post("/extract-text/")
async def extract_text(file: UploadFile = File(...), app_settings=Depends(get_settings)):

    image_bytes  = await file.read()

    ocr_object = Pytesseract()
    extracted_text = ocr_object.read_image(image_bytes )
    return {
        "filename": file.filename,
        "extracted_text": extracted_text
    }



@data_router.post("/extract-text-mistral/")
async def extract_text(file: UploadFile = File(...), app_settings=Depends(get_settings)):

    image_bytes  = await file.read()

    ocr_object = MistralOCR()
    extracted_text = ocr_object.read_image(image_bytes)
    return {
        "filename": file.filename,
        "extracted_text": extracted_text
    }

@data_router.get("/try_relevance")
async def relevance(request: Request):

    return await check_relevance(engine= request.app.db_engine)