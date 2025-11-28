import json
from ..tools import email_sender
from stores.llm import GroqProvider
from agents.ReportAgent.utils.ReportState import ReportState
import logging



async def node_sending_email(state: ReportState):

    receiver = state.get('email','')

    message = """You are an assistant that sends email to our users who asked a question about their last transactions in our application which interests in personal finance tracking.
    \n
    you will accept the user name and the user question and the formated report that a previous node created based on the user's question.
    \n
    
    user_question:{user_question}
    \n
    report_content: {report_content}
    \n
    user_name: {user_name}
    \n


    
    Use them to create a concise email that includes a subject and a body in HTML format. and the name of the receiver.
    \n
    and the company name is callend MyWallet.
    \n
    Your task is to create a JSON format for the following keys:

    title: email title that summarizes the report

    subject: email subject that grabs the user's attention

    body: HTML format answer (make the body as human readable and in HTML format to use it in the sender).

    """.format(user_question=state.get('question',''), report_content=state.get('report_content',''), user_name=state.get('user_name',''))

    

    



    instance = await GroqProvider.create_instance()
    llm = instance.client
    # prefer async invocation
    try:
        contentt = await llm.ainvoke(message)
        content_str = contentt.content if hasattr(contentt, 'content') else contentt
    except Exception:
        # fallback to sync invoke if async invocation is not available
        contentt = llm.invoke(message)
        content_str = contentt.content if hasattr(contentt, 'content') else contentt

    try:
        parsed_output = json.loads(content_str) if isinstance(content_str, str) else (content_str or {})
    except Exception:
        parsed_output = {}

    body = parsed_output.get('body', '')
    subject = parsed_output.get('subject', '')
    title = parsed_output.get('title', '')

    email_sender(receiver,title,subject,body)

    state['email_sent'] = parsed_output
    state['content'] = content_str
    logging.getLogger(__name__).info(f"send_email node output length: {len(str(content_str))}")
    return state