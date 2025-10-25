from ..state import AgentState
from langchain_core.runnables import RunnableConfig
from sqlalchemy import text

async def execute_sql(state: AgentState, config: RunnableConfig):
    sql_query = state.get('sql_query', '').strip()
    if not sql_query:
        state['query_result'] = "No SQL query provided"
        state['sql_error'] = True
        return state

    # Expect a sessionmaker (async) under 'db_client' or an engine under 'engine'
    db_client = config['configurable'].get('db_client')  # sessionmaker
    engine = config['configurable'].get('engine')  # AsyncEngine fallback

    try:
        if db_client:
            # sessionmaker (AsyncSession)
            async with db_client() as session:
                if sql_query.lower().startswith("select"):
                    result = await session.execute(text(sql_query))
                    columns = result.keys()
                    rows = result.mappings().all()  # list[Mapping]
                    state['query_rows'] = [dict(r) for r in rows]

                    header = ' | '.join(columns)
                    row_lines = [
                        ' | '.join(str(r.get(c)) if r.get(c) is not None else '' for c in columns)
                        for r in rows
                    ]
                    state['query_result'] = header + ('\n' + '\n'.join(row_lines) if row_lines else '')
                    state['sql_error'] = False
                else:
                    # write query: run inside a transaction so changes are committed
                    async with session.begin():
                        await session.execute(text(sql_query))
                    state['query_result'] = "OK"
                    state['query_rows'] = []
                    state['sql_error'] = False

        elif engine:
            # AsyncEngine path: obtain connection and run
            async with engine.connect() as conn:
                if sql_query.lower().startswith("select"):
                    result = await conn.execute(text(sql_query))
                    columns = result.keys()
                    rows = result.mappings().all()
                    state['query_rows'] = [dict(r) for r in rows]

                    header = ' | '.join(columns)
                    row_lines = [
                        ' | '.join(str(r.get(c)) if r.get(c) is not None else '' for c in columns)
                        for r in rows
                    ]
                    state['query_result'] = header + ('\n' + '\n'.join(row_lines) if row_lines else '')
                    state['sql_error'] = False
                else:
                    # needs transaction for writes
                    async with conn.begin():
                        await conn.execute(text(sql_query))
                    state['query_result'] = "OK"
                    state['query_rows'] = []
                    state['sql_error'] = False
        else:
            state['query_result'] = "No db_client or engine provided in config"
            state['sql_error'] = True

    except Exception as e:
        state['query_result'] = f"Error executing SQL query: {str(e)}"
        state['sql_error'] = True

    return state