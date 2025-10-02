import os 
import shutil
from controllers.BaseController import BaseController
import uuid
from fastapi import UploadFile



class DataController(BaseController):
    def __init__(self):
        super().__init__()

    @classmethod
    async def create_instance(cls):
        return cls()    
        
    async def save_uploaded_file(self,user_id: int ,file: UploadFile) -> str:
        # Ensure the data directory exists
        self.data_dir = os.path.join(self.data_dir, f"user_{user_id}")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Generate a unique filename to avoid collisions
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.data_dir, unique_filename)

        # Save the uploaded file to the data directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path