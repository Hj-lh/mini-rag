from helpers.config import get_settings
import os
import random
import string
class BaseController:
    def __init__(self):
        self.settings = get_settings()

        # Get the src directory (parent of controllers directory)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )

    def generate_random_string(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))