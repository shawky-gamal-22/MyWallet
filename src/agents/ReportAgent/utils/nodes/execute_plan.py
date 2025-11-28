from ..tools import aggregate_sum, group_count, top_k_items
from agents.ReportAgent.utils.ReportState import ReportState
import logging


async def execute_plan(state: ReportState) -> dict:
    logger = logging.getLogger(__name__)
    logger.info(f"execute_plan start: tools={state.get('tools')}")
    results = {}
    for tool in state.get("tools", []):
        name = tool.get("name")
        args = tool.get("args", {})
        if name == "aggregate_sum":
            result = aggregate_sum(state.get("query_rows", []), args.get("field"))
        elif name == "group_count":
            result = group_count(state.get("query_rows", []), args.get("field"))
        elif name == "top_k_items":
            result = top_k_items(state.get("query_rows", []), args.get("field"), args.get("k", 5))
        else:
            result = None
        results[name] = result

    state["tool_results"] = results
    logger.info(f"execute_plan done: tool_results keys={list(results.keys())}")
    return state