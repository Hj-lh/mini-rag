from ..LLMInterface import LLMInterface
from openai import OpenAI
import logging

class OllamaProvider(LLMInterface):

    def __init__(self, api_key: str=None, base_url: str=None, default_input_max_characters: int=5000, default_output_max_tokens: int=5000, default_temperature: float=0.7):
        self.api_key = api_key
        self.base_url = base_url if base_url else "http://localhost:11434"

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        self.generation_model = None
        self.embedding_model = None
        self.embedding_size = None

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id:str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(self, prompt: str, max_output_tokens: int=None, temperature: float=None):
        raise NotImplementedError("OllamaProvider does not support text generation yet.")
    
    def embed_text(self, text: str, document_id: str):
        if not self.client:
            self.logger.error("Ollama client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Invalid response from Ollama embeddings API.")
            return None
        
        return response.data[0].embedding