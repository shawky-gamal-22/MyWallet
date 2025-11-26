from typing_extensions import TypedDict



class ReportState(TypedDict):

    question: str
    report_type: str
    report_content: str
    user_id: int
    user_name: str
    email: str
    query_result: str
    query_rows: list
    report_type: str
    tools: list
    formatter_hints: dict
    tool_results: dict
    email_sent: bool
    
  