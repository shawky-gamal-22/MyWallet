from controllers.BaseController import BaseController
from agents.SQLAgent import SQLAgent

class AgentController(BaseController):

    def __init__(self):
        super().__init__()

    @classmethod
    async def create_instance(cls):
        return cls()  
    

    async def AgentInvoke(self, question: str, user_id:int, engine, db_clinet):

        sql_agent = await SQLAgent.create_instance()

        result = await sql_agent.invoking(question= question, 
                                          user_id = user_id, 
                                          engine = engine,
                                          db_clinet = db_clinet)

        if result :
            return result 