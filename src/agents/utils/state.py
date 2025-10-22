from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class AgentState(BaseModel):

    question: str
    sql_query: str
    query_result: str
    query_rows: list
    user_id: int
    user_name: str
    attempts: int 
    relevence: str
    sql_error: bool
    schema: str