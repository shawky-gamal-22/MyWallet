import json
from ..tools import email_sender
from stores.llm import GroqProvider
from src.agents.ReportAgent.utils.ReportState import ReportState



async def node_sending_email(state: ReportState):

    receiver = state.get('email','')
    queries = state.get('query_result','')
    user_question = state.get('question', '')
    system = """You are an assistant that sends email to our users who asked a question about their last transactions in our application which interests in personal finance tracking.
    \n
    you will accept queries that is fetched from the database according the user question.
    
    
    Use the  question and the queries to make an email to send to the user.

    create a json format for the following content:
    subject: str (make it clear and short)
    body: HTML (make the body as human readable and in HTML format to use it in the sender).

    """.format(user_question=user_question,queries=queries)

    human = f"Question: {user_question}\n\n Queries: {queries}"

    messages = [
        ("system", system),
        ("human", human),
    ]



    instance = await GroqProvider.create_instance()
    llm = instance.client
    content = await llm.invoke(messages)

    parsed_output = json.loads(content.content)

    body = parsed_output['body']
    subject = parsed_output['subject']

    email_sender(receiver,subject,body)

    state['email_sent'] = True
    return state