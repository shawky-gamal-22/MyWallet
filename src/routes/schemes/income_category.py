from pydantic import BaseModel


class IncomeCategoryRequest(BaseModel):
    name: str

    description: str | None = None

