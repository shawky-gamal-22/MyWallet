from controllers.BaseController import BaseController
from agents.SQLAgent import SQLAgent
from agents.ReportAgent import ReportAgent

class AgentController(BaseController):

    def __init__(self):
        super().__init__()

    @classmethod
    async def create_instance(cls):
        return cls()  
    

    async def AgentInvoke(self, question: str, user_id:int, engine:object, db_client:object):

        sql_agent = await SQLAgent.create_instance()

        result = await sql_agent.invoking(question= question, 
                                          user_id = user_id, 
                                          engine = engine,
                                          db_client = db_client)
        return result

    
    async def ReportAgentInvoke(self, question: str, user_id:int, engine:object, db_client:object):

        report_agent = await ReportAgent.create_instance()

        report = await report_agent.invoking(question= question, 
                           user_id = user_id, 
                           engine = engine,
                           db_client = db_client)

        return report