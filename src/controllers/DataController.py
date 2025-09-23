import os
from .BaseController import BaseController
from fastapi import UploadFile
from .ProjectController import ProjectController
import re
class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_UploadedFile(self, file: UploadFile):

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, f"File type {file.content_type} is not allowed."
        
        if file.size > self.settings.FILE_MAX_SIZE:
            return False, f"File size exceeds the maximum limit of {self.settings.FILE_MAX_SIZE} bytes."

        return True, "success"

    def generate_unique_filename(self, original_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(original_file_name=original_file_name)

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path

    def get_clean_file_name(self, original_file_name: str):
        # Remove special characters and spaces from the file name
        cleaned_file_name = re.sub(r'[^w.]','', original_file_name.strip())
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        return cleaned_file_name
