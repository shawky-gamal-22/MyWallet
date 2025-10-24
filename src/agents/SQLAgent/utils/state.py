from typing_extensions import TypedDict
from pydantic import BaseModel, Field



class AgentState(TypedDict):

    question: str
    sql_query: str
    query_result: str
    query_rows: list
    user_id: int
    user_name: str
    attempts: int 
    relevance: str
    schema: str
    sql_error: bool
  