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


class UpdateRequest(BaseModel):
    income_id : int
    category_name: str | None = None
    source_name: str| None = None
    amount: float | None = None
    is_recurring: bool| None = None

    description: str | None = None
    recurrence_interval: str | None = None
    next_due_date: str | None = None


class UpdateNextDueDateRequest(BaseModel):
    income_id: int
    next_due_date: str
