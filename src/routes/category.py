from fastapi import  APIRouter, Request
from models import CategoryModel
from models.enums import ResponseStatus
from .schemes import CategoryRequest


category_router = APIRouter()

@category_router.post("/create-category/")
async def create_category(request: Request, category: CategoryRequest):

    category_model_instance = await CategoryModel.create_instance(request.app.db_client)
    created_category = await category_model_instance.create_category(
        name=category.name,
        description=category.description
    )

    if created_category is None:
        return{
            "status": ResponseStatus.CATEGORY_ALLREADY_EXISTS.value
        }
    else:
        return {
            "status": ResponseStatus.CATEGORY_ADDED_SUCCESS.value,
            "category_id": created_category.id
            }
