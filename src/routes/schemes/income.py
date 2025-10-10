from pydantic import BaseModel


class IncomeRequest(BaseModel):
    category_name: str
    source_name: str
    amount: float 
    is_recurring: bool

    description: str | None = None
    recurrence_interval: str | None = None
    next_due_date: str | None = None

class DeleteRequest(BaseModel):
    income_id: int