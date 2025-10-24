from fastapi import FastAPI, Depends, APIRouter, UploadFile, File, Request
from helpers.config import get_settings
from stores.OCR import Pytesseract, MistralOCR
from controllers import AgentController
from .schemes import AgentRequest

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

@data_router.post("/try_relevance/{user_id}")
async def relevance(request: Request, user_id: int, agent_req:AgentRequest):
    agent_controller = await AgentController.create_instance()

    result = await agent_controller.AgentInvoke(question= agent_req.question, 
                                                user_id= user_id, 
                                                engine = request.app.db_engine,
                                                db_clinet = request.app.db_client)

    return result 