from helpers.config import get_settings
import os

class BaseController:
    def __init__(self):
        self.settings = get_settings()

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.base_dir, "assets","images")
        self.assets_dir = "assets/images"