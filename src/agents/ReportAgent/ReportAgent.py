from langgraph.graph import StateGraph, START, END
from .utils import ReportState
from .utils.nodes import (
    sql_node,
    execute_plan,
    format_report,
    node_sending_email
)


class ReportAgent:
    def __init__(self):
        self.agent = StateGraph(ReportState)

        self.agent.add_node("sql_node", sql_node)
        self.agent.add_node("execute_plan", execute_plan)
        self.agent.add_node("format_report", format_report)
        self.agent.add_node("node_sending_email", node_sending_email)

        self.agent.add_edge(START, "sql_node")
        self.agent.add_edge("sql_node", "execute_plan")
        self.agent.add_edge("execute_plan", "format_report")
        self.agent.add_edge("format_report", "node_sending_email")
        self.agent.add_edge("node_sending_email", END)
        self.ReportAgent = self.agent.compile()


    @classmethod
    async def create(cls):
        return cls()
    

    async def invoke(self, question: str, user_id: int, engine:object, db_client:object):
        """Invoke the compiled agent with the provided question and user id.

        Parameters are ordered to match callers that use keyword args
        (question=..., user_id=...).
        """
        config = {"configurable": {"user_id": user_id, "engine": engine, "db_client": db_client}}
        
        return await self.ReportAgent.ainvoke(
            {"question": question,
             "user_id": user_id},
            config=config,
        )