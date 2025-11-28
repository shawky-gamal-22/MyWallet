from sqlalchemy import inspect
from ..state import AgentState
from stores.llm import GroqProvider
from langchain_core.runnables import RunnableConfig
import json


async def get_schema(engine):
    """Return a textual representation of the database schema.

    This function opens an async connection from the provided AsyncEngine
    and runs synchronous inspection code via `conn.run_sync`.
    """

    async with engine.connect() as conn:
        def _build_schema(sync_conn):
            inspector = inspect(sync_conn)
            schema_lines = []
            table_names = inspector.get_table_names()

            for table_name in table_names:
                schema_lines.append(f"Table: {table_name}")
                fks = inspector.get_foreign_keys(table_name)
                pks = inspector.get_pk_constraint(table_name)
                pks_names = pks['constrained_columns']
                fk_names = []
                fk_info = {}
                
                for i,fk in enumerate(fks):
                    
                    fk_name = fk['constrained_columns'][0]
                    fk_names.append(fk_name)
                    fk_table = fk['referred_table']
                    fk_col = fk['referred_columns'][0]
                    foreign_key_info = f"  Foreign Key to table {fk_table} for Column named {fk_col}"
                    
                    fk_info[fk_name] = foreign_key_info

                columns = inspector.get_columns(table_name)
                for column in columns:
                    
                    col_name = column.get("name")
                    col_type = str(column.get("type"))

                    if col_name in pks_names:
                        col_type += f" Primary Key"
                    
                    if col_name in fk_names:
                        col_type += fk_info[col_name]
                    
                    schema_lines.append(f"- {col_name}: {col_type}")
              
                schema_lines.append("")

            return "\n".join(schema_lines)

        schema = await conn.run_sync(_build_schema)

    return schema


#node
async def check_relevance(SqlState: AgentState, config: RunnableConfig):
    question = SqlState['question']
    #question = "What is the last receipt for me?"
    engine = config['configurable'].get("engine", None)
    schema = await get_schema(engine)
    SqlState['schema'] = schema

    system = """You are an assistant that determines whether a given question is related to the following database schema.

    Schema:
    {schema}



    You should know that Invoice table have other words with the same meaning like receipt, bill, etc.... take care of something like this.

    Respond with only "relevant" or "not_relevent" with key "relevance" in JSON Format.
    """.format(schema=schema)

    human = f"Question: {question}"

    messages = [
        ("system", system),
        ("human", human),
    ]

    # create_instance is async; await it
    instance = await GroqProvider.create_instance()
    llm = instance.client

    relevance = llm.invoke(messages)
    parsed_output = json.loads(relevance.content)

    SqlState['relevance'] = parsed_output['relevance']
    return SqlState


#router

async def relevance_router(SqlState: AgentState):

    if SqlState['relevance'].lower() =="relevant":
        return "convert_to_sql"
    else:
        return "return_state"