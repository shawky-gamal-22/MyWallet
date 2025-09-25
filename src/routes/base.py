from fastapi import FastAPI, Depends, APIRouter
from helpers.config import get_settings
from datetime import datetime

base_router = APIRouter()

@base_router.get("/")
async def welcome(app_settings=Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }