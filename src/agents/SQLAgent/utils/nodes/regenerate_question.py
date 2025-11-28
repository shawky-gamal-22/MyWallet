from ..state import AgentState
from stores.llm import GroqProvider
import json


async def regenerate_question(SqlState: AgentState):

    try:

        question = SqlState.get("question")
        schema = SqlState.get("schema")

        system = """You are an assistant that reformulates an original question from the user to enable more precise SQL queries.
                    Ensure that all necessary details, such as table join, are preserved to retrieve complete and accurate data.

                    This is the schema of the database to know it when regenrating the question:

                    {schema}

                    Answer in JSON Format with key 'question'.
        """.format(schema= schema)

        human = """Original question: {question}\n Reformulate the question to enable more precise SQL queries, ensuring all necessary detail, are preserved.""".format(question= question)

        messages = [
            ("system", system),
            ("human", human)
        ]

        instance = await GroqProvider.create_instance()
        llm = instance.client

        answer = llm.invoke(messages)
        parsed_answer = json.loads(answer.content)

        SqlState['question'] = parsed_answer['question']
        SqlState["attempts"] += 1

        return SqlState 
    except Exception as e:

        SqlState['sql_error'] = True
        SqlState['question'] = f"Can not reformulte the question due to this error {e}"
        return SqlState

async def end_max_iterations(SqlState: AgentState):
    SqlState["query_result"] = "Please try again."
    return SqlState 

async def execute_sql_router(SqlState: AgentState):

    if  SqlState.get("sql_error", False):
        return "regenerate_question"
    else :
        return "return_state"
    
    
async def check_attempts_router(SqlState: AgentState):
    if SqlState.get("attempts",0) < 3:
        return "convert_to_sql"
    else :
        return "end_max_iterations"

