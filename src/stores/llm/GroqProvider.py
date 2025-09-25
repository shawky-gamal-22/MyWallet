from langchain_groq import ChatGroq
from helpers.config import Settings, get_settings

class GroqProvider:
    def __init__(self,temperature: float = 0.0,max_tokens: int = 1024, timeout: int = None, max_retries: int = 2):
        self.settings: Settings = get_settings()
        self.client = ChatGroq(api_key=self.settings.GROQ_API_KEY,
                               model=self.settings.GENERATION_MODEL_ID,
                               temperature=temperature,
                               max_tokens=max_tokens,
                               timeout=timeout,
                               max_retries=max_retries,
                               response_format={"type": "json_object"})
        
    
    def generate_row(self, extracted_text):

        miessages = [
            (
                "system",
                "You are a tabular data extractor that extracts tabular data from text and returns it in JSON format.\n\n You will get text extract the following fields:\n\n"
                "The name of the operation\n in a key called 'operation_name'\n\n"
                "The total amount of the operation in a key called 'total_amount'\n\n"
                ""
            ),
            ("human", extracted_text)
        ]
        response = self.client.invoke(miessages)

        return response.content