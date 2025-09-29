from pydantic import BaseModel


class InvoiceRequest(BaseModel):
    user_id: int
    category_id: int
    total_price: float
    description: str | None = None
    img_path: str | None = None


    
from pydantic import BaseModel

class DateRangeRequest(BaseModel):
    start_date: str
    end_date: str