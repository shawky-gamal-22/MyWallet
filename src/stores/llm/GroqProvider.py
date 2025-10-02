from langchain_groq import ChatGroq
from helpers.config import Settings, get_settings
from typing import List

class GroqProvider:
    def __init__(self,temperature: float = 0.0,max_tokens: int = 1024, timeout: int = None, max_retries: int = 2):
        self.settings: Settings = get_settings()
        self.client = ChatGroq(api_key=self.settings.GROQ_API_KEY,
                               model=self.settings.GENERATION_MODEL_ID,
                               temperature=0.5,
                               max_tokens=max_tokens,
                               timeout=timeout,
                               max_retries=max_retries,
                               
                               response_format={"type": "json_object"})
        
    @classmethod
    async def create_instance(cls):
        return cls() 
        
    
    async def generate_row(self, extracted_text: str, user_id: int, categories: List[dict]) -> dict:

        category_list = (
            "the following list based on the extracted text:\n\n"
            + "\n".join([f"{category['id']}: {category['name']} - {category['description']}" for category in categories])
            + "\n\n"
        )

        the_user_id = f"The user_id is {user_id}.\n\n"
        miessages = [
            (
                "system",
                "You are a tabular data extractor that extracts tabular data from text and returns it in JSON format.\n\n You will get a text, extract the following fields:\n\n"
                "\n\n"
                "The ID of the user who owns the operation in a key called 'user_id'"
                "The category ID of the operation in a key called 'category_id'"
                "The name of the operation in a key called 'invoice_name'"
                "The total amount of the operation in a key called 'total_price'"
                "The description of the operation in a key called 'description' and the value will be  a short description of the operation and include the price\n"
                "\n\n"
                f"For the category_id, you will choose the most appropriate category from {category_list}\n\n"
                "Provide the answer with only keys and values, no additional text.\n\n"
            ),
            ("human",the_user_id + extracted_text)
        ]
        response = self.client.invoke(miessages)

        return response.content
    

    async def summary_invoices_range_date(self, user_id: int, 
                                          start_date: str, 
                                          end_date: str, 
                                          invoices: List[dict],
                                          total_spent: float) -> dict:
        miessages = [
            (
                "system",
                "You are a financial assistant that provides a summary of invoices for a user within a specified date range. "
                "You will receive the start date, and end date, the invoices done in that range in a list of dictionaries, and the total money spent in that range, and you need to return a summary of what happened in that date range,"
                "including the total number of invoices and the total amount spent. "
                "Provide the answer with a nicely formatted text, and include the total number of invoices and the total amount spent. "
                "Inclue the all the invoice categories and the total spent in each category. "
                "proide a good summary of the user's spending habits during that period. "
                "Inclue the answer in a JSON object with a key called 'summary'."
            ),
            (
                "human",
                f"The start date is {start_date} and the end date is {end_date}, "
                f"The invoices are: {invoices}, and the total money spent is {total_spent}."
            )
        ]
        response = self.client.invoke(miessages)

        return response.content