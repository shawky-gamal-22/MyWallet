import base64
import os
from mistralai import Mistral
from helpers.config import get_settings

class MistralOCR:

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.MISTRAL_API_KEY
        self.client = Mistral(api_key=self.api_key)

    @classmethod
    async def create_instance(cls):
        return cls()

    async def read_image(self, image_bytes: bytes) -> str:
        b64 = base64.b64encode(image_bytes).decode('utf-8')

        resp = self.client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{b64}"
            },
            include_image_base64=True
            )
        
        return resp.pages[0].markdown