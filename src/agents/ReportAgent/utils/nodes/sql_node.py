from agents.SQLAgent import SQLAgent
#from controllers import AgentController
from ..ReportState import ReportState
from langchain_core.runnables import RunnableConfig
import logging

async def sql_node(state: ReportState, config: RunnableConfig):
    logger = logging.getLogger(__name__)
    agent_controller = await SQLAgent.create_instance()
    logger.info(f"sql_node start: question={state.get('question')} user_id={config['configurable'].get('user_id')}")

    try:
        result = await agent_controller.invoking(
            question= state.get('question', ''),
            user_id= config['configurable'].get('user_id', None), 
            engine = config['configurable'].get("engine", None),
            db_client = config['configurable'].get('db_client')
        )
        logger.info(f"SQLAgent result type: {type(result)}")
        logger.info(f"SQLAgent result: {result}")

        if result is None:
            logger.error("SQLAgent returned None!")
            state['query_result'] = "Error: SQL Agent returned no result"
            state['query_rows'] = []
            state['email'] = ''
            state['user_name'] = ''
            state['user_id'] = config['configurable'].get('user_id', None)
            return state

        # Safely extract data from result
        state["query_result"] = result.get("query_result", "")
        state["query_rows"] = result.get("query_rows", [])
        state['email'] = result.get('user_email', '')
        state['user_name'] = result.get('user_name', '')
        state['user_id'] = config['configurable'].get('user_id', None)
        logger.info(f"sql_node done: rows={len(state.get('query_rows', []))}")
        
    except Exception as e:
        # report error into state and continue pipeline
        state['query_result'] = f"Error invoking SQL agent: {e}"
        state['query_rows'] = []
        state['email'] = ''
        state['user_name'] = ''
        state['user_id'] = config['configurable'].get('user_id', None)
        return state


    return state