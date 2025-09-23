from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_UploadedFile(self, file: UploadFile):

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, f"File type {file.content_type} is not allowed."
        
        if file.size > self.settings.FILE_MAX_SIZE:
            return False, f"File size exceeds the maximum limit of {self.settings.FILE_MAX_SIZE} bytes."

        return True, "success"