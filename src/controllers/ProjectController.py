from .BaseController import BaseController
from fastapi import FastAPI

class ProjectController(BaseController):

    def __init__(self):
        super().__init__()