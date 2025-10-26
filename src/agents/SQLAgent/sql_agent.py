from langgraph.graph import StateGraph, START, END
from .utils import AgentState
from .utils.nodes import (
    get_current_user,
    check_relevance,
    relevance_router,
    convert_to_sql,
    execute_sql,
    regenerate_question,
    execute_sql_router,
    check_attempts_router,
    end_max_iterations,
    return_state
)

class SQLAgent:
    
    def __init__(self):

        self.agent = StateGraph(AgentState)

        self.agent.add_node("get_current_user", get_current_user)
        self.agent.add_node("check_relevance", check_relevance)
        self.agent.add_node("convert_to_sql", convert_to_sql)
        self.agent.add_node("execute_sql", execute_sql)
        self.agent.add_node("regenerate_question", regenerate_question)
        self.agent.add_node("end_max_iterations", end_max_iterations)
        self.agent.add_node("return_state", return_state)


        self.agent.add_edge(START,"get_current_user")
        self.agent.add_edge("get_current_user","check_relevance")

        self.agent.add_conditional_edges(
            "check_relevance",
            relevance_router,
            {
                "convert_to_sql":"convert_to_sql",
                "return_state": "return_state"
                
            }
        )
        self.agent.add_edge("convert_to_sql", "execute_sql")
        self.agent.add_conditional_edges(
            "execute_sql",
            execute_sql_router,
            {
                "regenerate_question": "regenerate_question",
                "return_state": "return_state",
            }
        )
        self.agent.add_conditional_edges(
            "regenerate_question",
            check_attempts_router,
            {
                "convert_to_sql": "convert_to_sql",
                "end_max_iterations": "end_max_iterations",
            }
        )
        
        self.agent.add_edge("end_max_iterations", END)
        self.agent.add_edge("return_state", END)
        self.SQLAgent = self.agent.compile()

    @classmethod
    async def create_instance(cls):
        return cls()

    async def invoking(self, question: str, user_id: int, engine, db_clinet):
        """Invoke the compiled agent with the provided question and user id.

        Parameters are ordered to match callers that use keyword args
        (question=..., user_id=...).
        """
        # Use the key name expected by the agent node `get_current_user` (it looks for 'user_id')
        config = {"configurable": {"user_id": user_id, "engine": engine, "db_client": db_clinet}}

        # call the async agent invocation
        result = await self.SQLAgent.ainvoke({"question": question}, config=config)

        # return the full result so callers can inspect (or change to specific field as needed)
        return result