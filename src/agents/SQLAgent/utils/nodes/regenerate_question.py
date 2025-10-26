from ..state import AgentState
from stores.llm import GroqProvider
import json


async def regenerate_question(state: AgentState):

    try:

        question = state.get("question")
        schema = state.get("schema")

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

        state['question'] = parsed_answer['question']
        state["attempts"] += 1

        return state 
    except Exception as e:

        state['sql_error'] = True
        state['question'] = f"Can not reformulte the question due to this error {e}"
        return state

async def end_max_iterations(state: AgentState):
    state["query_result"] = "Please try again."
    return state 

async def execute_sql_router(state: AgentState):

    if  state.get("sql_error", False):
        return "regenerate_question"
    else :
        return "return_state"
    
    
async def check_attempts_router(state: AgentState):
    if state['attempts'] < 3:
        return "convert_to_sql"
    else :
        return "end_max_iterations"

