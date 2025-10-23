from ..state import AgentState
from langchain_core.runnables import RunnableConfig
from models import UserModel
from fastapi import Request




# node
async def get_current_user(state: AgentState, config: RunnableConfig, request: Request):
    user_id = config["configurable"].get("user_id",None)

    if not user_id:
        state['user_id'] = "user not found"

    try:
    
        user_model = await UserModel.create_instance(db_client= request.app.db_client)

        user = await user_model.get_user_by_id(user_id= user_id)

        if user:
            state['user_name'] = user.username
            state['user_id'] = user_id
        else:
            state['user_name'] = "user not found"

        return state
    except:
        state['user_name'] ="Error while fetching the user name"



