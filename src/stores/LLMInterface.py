from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_name:str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_name:str, embedding_size:int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, max_output_tokens: int, temperature: float):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_id: str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass