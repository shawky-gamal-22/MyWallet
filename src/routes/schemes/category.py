from pydantic import BaseModel


class CategoryRequest(BaseModel):
    name: str
    description: str
