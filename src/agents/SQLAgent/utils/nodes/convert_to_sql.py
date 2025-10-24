from ..state import AgentState
from stores.llm import GroqProvider
import json



#node
async def convert_to_sql(state: AgentState):

    question = state.get('question')
    current_user = state.get('user_id')
    schema = state.get('schema')

    system = """You are an assistant that converts natural language questions into SQL queries based on the following schema:

    {schema}

    The current user his id is {current_user} , the id is integer. Ensure that all query-related data is scoped to this user id.

    Provide only the SQL query without any explanations. With a key named 'sql_query' in JSON Format.

    Alias columns appropriately to match the expected keys in teh result.

    For example, alias 'food.name' as 'food_name' and 'food.price' as 'price'.
    """.format(schema=schema, current_user=current_user)

    human = f"Question: {question}"

    messages= [
        ('system', system),
        ('human', human)
    ]

    # create_instance is async; await it
    instance = await GroqProvider.create_instance()
    llm = instance.client

    answer = llm.invoke(messages)
    parsed_answer = json.loads(answer.content)

    state['sql_query'] = parsed_answer['sql_query']

    return state