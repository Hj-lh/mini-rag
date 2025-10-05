from .LLMEnums import LLMEnums, LLMProvider
from .providers import OllamaProvider


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLMProvider.OLLAMA.value:
            return OllamaProvider(
                api_key=self.config.OPENAI_API_KEY,
                base_url=self.config.OLLAMA_API_URL,
                
            )
        
    