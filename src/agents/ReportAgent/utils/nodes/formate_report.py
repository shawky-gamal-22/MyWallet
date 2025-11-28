from stores.llm import GroqProvider
from agents.ReportAgent.utils.ReportState import ReportState
import logging


async def format_report(state: ReportState) -> str:
    
    message = """You are the Report Formatter Agent.

Your task is to take:
1. The question of the user.
2. The aggregated result produced by the Aggregation Layer.
3. Metadata about what operations were performed.
4. (Optional) Raw rows used for the calculation.

Your ONLY job is to produce a clear, concise, human-readable report.

Follow these rules strictly:

- Do NOT invent numbers.
- Do NOT run new calculations or aggregations.
- Only describe and explain the results already provided.
- Summaries must be structured, readable, and actionable.
- Use bullet points and short paragraphs when appropriate.
- If the user question implies a comparison, trend, summary, or insight,
  only describe what can be inferred from the existing aggregated result.
- If the result is empty, say so and suggest what data may be missing.

Your report MUST contain the following structure:

---
### **Report**
**User Question:** <insert user question>

**Summary of Findings:**
- Plain-English explanation of the aggregated result.
- Describe the meaning of the computed metrics.
- Highlight the most important insight the user needs.

**Details:**
- Numerical results, formatted as bullet points.
- If groupings exist (e.g., by category), display them in a clean table-style list.

**Notes:**
- Mention any limitations (e.g., small dataset, no matching records).
- If helpful, suggest follow-up questions the user could ask.

---

Here is the data you must use:
- User Question: {user_question}
- Aggregated Result JSON: {aggregated_result}
- Metadata: {metadata}
- Raw Rows (may be empty): {raw_data}
""".format(user_question=state.get('question', ''), aggregated_result=state.get('tool_results', {}), metadata=state.get('formatter_hints', {}), raw_data=state.get('query_rows', []))
    
    # create_instance is async; await it
    instance = await GroqProvider.create_instance()
    llm = instance.client
    report = await llm.ainvoke(message)
    content_str = report.content if hasattr(report, 'content') else report

    state['report_content'] = content_str
    state['report_format'] = 'html'
    logging.getLogger(__name__).info(f"Formatted report content length: {len(str(content_str))}")
    return state