from typing_extensions import TypedDict
from typing import Any, List, Dict


class ReportState(TypedDict, total=False):

    question: str
    report_type: str
    report_content: str
    user_id: int
    user_name: str
    email: str
    query_result: str
    query_rows: List[Dict[str, Any]]
    tools: List[str]
    formatter_hints: Dict[str, Any]
    tool_results: Dict[str, Any]
    email_sent: bool
    report_format: str
    content: str
    
  