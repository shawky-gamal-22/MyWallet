from ..state import AgentState
from langchain_core.runnables import RunnableConfig
from models import UserModel
from fastapi import Request




# node
async def get_current_user(SqlState: AgentState, config: RunnableConfig):
    user_id = config["configurable"].get("user_id",None)
    db_client = config['configurable'].get('db_client', None)
    SqlState['user_id'] = user_id
    if not user_id:
        SqlState['user_id'] = None

    try:
    
        user_model = await UserModel.create_instance(db_client= db_client)

        user = await user_model.get_user_by_id(user_id= user_id)

        if user:
            SqlState['user_name'] = user.username
            SqlState['user_email'] = user.email
            
        else:
            SqlState['user_name'] = "user not found"
            SqlState['user_email'] = "user not found"

        return SqlState
    except:
        SqlState['user_name'] ="Error while fetching the user name"
        SqlState['user_email'] = "Error while fetching the user email"
        return SqlState



