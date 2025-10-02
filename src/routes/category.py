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

@category_router.get("/get-all-categories/")
async def get_all_categories(request: Request):

    has_records = True
    result = []
    page_no = 1
    page_size = 10

    category_model_instance = await CategoryModel.create_instance(request.app.db_client)
    while has_records:
        categories = await category_model_instance.get_all_categories(page_no= page_no, page_size= page_size)
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

    return {
        "status": ResponseStatus.GET_ALL_CATEGORIES_SUCCESS.value,
        "data": result
    }
