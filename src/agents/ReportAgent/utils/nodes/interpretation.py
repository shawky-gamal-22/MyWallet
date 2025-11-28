from stores.llm import GroqProvider
import json
import logging
from agents.ReportAgent.utils.ReportState import ReportState



async def interpretation_node(state:ReportState):
    message = """You are an assistant that MUST output only JSON conforming to the Plan schema described below.


        Input:
        - user_query: {user_query}
        - raw_rows: {raw_rows}

        Rules:
        1) Decide the report_type: one of ["summary", "top_k", "comparison", "detailed_list"].
        2) Choose minimal set of tools from the toolbox: aggregate_sum, group_count, top_k_items.
        3) For each tool include: name, args, output_schema (simple JSON types).
        4) Do NOT compute final numbers; only declare the plan.
        5) Output a single JSON object and nothing else.

        Output Schema Example:
        {{
        "report_type": "comparison",
        "tools": [
            {{"name":"aggregate_sum","args":{{"field":"amount","group_by":null,"filter":{{"type":"current_period"}}}},"output_schema":{{"total":"float"}}}},
            ...
        ],
        "formatter_hints": {{"title":"...", "highlight":"..."}}
        }}
        """.format(user_query = state.get('question', ''), raw_rows= state.get('query_rows', []))


    # create_instance is async; await it
    instance = await GroqProvider.create_instance()
    llm = instance.client
    # prefer the async invocation and parse the returned content (which may be a JSON string)
    plan_response = await llm.ainvoke(message)
    plan_str = plan_response.content if hasattr(plan_response, 'content') else plan_response
    try:
        if isinstance(plan_str, dict):
            plan = plan_str
        else:
            plan = json.loads(plan_str)
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to parse plan JSON: {e}; plan_response: {plan_str}")
        plan = {}
    state["report_type"] = plan.get("report_type", "")
    state["tools"] = plan.get("tools", [])
    state["formatter_hints"] = plan.get("formatter_hints", {})

    return state