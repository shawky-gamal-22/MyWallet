from SQLAgent import create_instance
from src.agents.ReportAgent.utils.ReportState import ReportState
from langchain_core.runnables import RunnableConfig

async def sql_node(state: ReportState, config: RunnableConfig):
    agent_controller = await create_instance()
    
    
    result = await agent_controller.AgentInvoke(question= state.get('question', ''),
                                                user_id= state.get('user_id', None), 
                                                engine = config['configurable'].get("engine", None),
                                                db_client = config['configurable'].get('db_client'))
    

    state["query_result"] = result.get("query_result", " ")
    state["query_rows"] = result.get("query_rows", [])
    state['email']= result.get('user_email', '')
    state['user_name']= result.get('user_name', '')
    return state